import os
import sys
import subprocess
import threading
import pyperclip
import pyautogui
import time
import psutil
from pynput import mouse, keyboard
from googletrans import Translator

# --- Global Değişkenler ve Ayarlar ---
g_current_box_process = None
g_process_lock = threading.Lock()
g_latest_job_id = 0
g_job_id_lock = threading.Lock()
g_previous_clipboard = ""  # 1. DEĞİŞİKLİK: En son başarılı kopyalamanın içeriğini tutacak değişken
ceviri_aktif = True

# --- Yol Ayarları (Değişiklik yok) ---
EV_DIZINI = os.path.expanduser("~")
github_dizini = os.path.join(EV_DIZINI, "github", "MAIN", "ceviri")
py_yol_dosyasi = os.path.join(github_dizini, "python")
try:
    with open(py_yol_dosyasi, "r") as f:
        surum = f.read().lower().strip().replace(" ", "")
    dizi = surum.split(".")
    surum = f"{dizi[0]}.{dizi[1]}"
    yol = os.path.join(github_dizini, 'VenvNotlar', 'lib', f'python{surum}', 'site-packages')
    sys.path.insert(0, yol)
except Exception as e:
    print(f"[UYARI] Sanal ortam yolu ayarlanamadı: {e}")

translator = Translator()

def write_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(content))

def ekran_ortasi():
    genislik, yukseklik = pyautogui.size()
    return genislik // 2, yukseklik // 2

def launch_box(text_to_show, x_pos, y_pos):
    global g_current_box_process
    with g_process_lock:
        if g_current_box_process and psutil.pid_exists(g_current_box_process.pid):
            try: psutil.Process(g_current_box_process.pid).kill()
            except psutil.NoSuchProcess: pass
        
        write_to_file("metin", text_to_show)
        write_to_file("x", x_pos - 100)
        write_to_file("y", y_pos - 120)
        
        try:
            g_current_box_process = subprocess.Popen([sys.executable, 'box.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"box.py başlatılamadı: {e}")
            g_current_box_process = None

def perform_translation(kopyalanan_metin, x_pos, y_pos, job_id):
    try:
        ceviri = translator.translate(kopyalanan_metin, src='en', dest='tr')
        text_sonuc = ceviri.text.strip() if (ceviri and ceviri.text) else None
        
        with g_job_id_lock:
            if job_id != g_latest_job_id:
                print(f"İş #{job_id} iptal edildi, çünkü daha yeni bir iş (#{g_latest_job_id}) var.")
                return
        
        if text_sonuc:
            print(f"Çeviri (#{job_id}): {text_sonuc}")
            launch_box(text_sonuc, x_pos, y_pos)

    except Exception as e:
        print(f"Çeviri hatası: {e}")

def on_click(x_coord, y_coord, button, pressed):
    global g_latest_job_id
    global g_previous_clipboard  # 2. DEĞİŞİKLİK: Global değişkene erişeceğimizi belirtiyoruz

    if not pressed and button == mouse.Button.left and ceviri_aktif:
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)
        
        kopyalanan_metin = pyperclip.paste()
        # strip() ile başındaki/sonundaki boşlukları temizleyerek karşılaştırıyoruz
        kopyalanan_metin_temiz = kopyalanan_metin.strip() if kopyalanan_metin else ""

        # 3. DEĞİŞİKLİK: ANA KONTROL
        # Sadece panoya YENİ bir metin kopyalandıysa ve bu metin boş değilse devam et.
        if kopyalanan_metin_temiz and kopyalanan_metin_temiz != g_previous_clipboard:
            # Panodaki metin yeni, bunu bir sonraki kontrol için kaydedelim.
            g_previous_clipboard = kopyalanan_metin_temiz
            
            with g_job_id_lock:
                g_latest_job_id += 1
                current_job_id = g_latest_job_id
            
            print(f"Yeni seçim algılandı (#{current_job_id}): '{kopyalanan_metin_temiz[:30]}...'")
            threading.Thread(
                target=perform_translation,
                args=(kopyalanan_metin_temiz, x_coord, y_coord, current_job_id)
            ).start()
        # else:
            # Eğer isterseniz, atlanan durumları görmek için bu satırı aktif edebilirsiniz.
            # print("Çeviri atlandı: Panoda yeni bir metin yok.")

# --- Klavye ve Temizlik Fonksiyonları (Değişiklik yok) ---
pressed_keys = set()
def on_press(key):
    global ceviri_aktif
    try:
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            pressed_keys.add("Alt")
        elif hasattr(key, 'char') and key.char.lower() == 'q':
            if "Alt" in pressed_keys:
                ceviri_aktif = not ceviri_aktif
                durum = "Çeviri Aktif" if ceviri_aktif else "Çeviri Pasif"
                print(f"Durum değiştirildi: {durum}")
                x_orta, y_orta = ekran_ortasi()
                launch_box(durum, x_orta, y_orta)
    except AttributeError: pass
def on_release(key):
    try:
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            pressed_keys.discard("Alt")
    except AttributeError: pass
def cleanup():
    print("\nTemizlik yapılıyor...")
    global g_current_box_process
    if g_current_box_process and psutil.pid_exists(g_current_box_process.pid):
        psutil.Process(g_current_box_process.pid).kill()
    print("Program sonlandırıldı.")

# --- Program Başlangıcı ---
if __name__ == "__main__":
    # Program başlarken panoyu temizlemek, ilk tıklamada eski bir şeyin gelmesini engeller.
    pyperclip.copy("")
    g_previous_clipboard = ""

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    print("\nÇeviri betiği başlatıldı.")
    print("-> Çevirmek için metin seçip (çift tıklayarak veya sürükleyerek) sol fare tuşunu bırakın.")
    print("-> ALT+Q tuşuyla çeviriyi açıp kapatabilirsiniz.")
    print("-> Programdan çıkmak için terminalde CTRL+C tuşlarına basın.")
    
    try:
        keyboard_listener.join()
    except KeyboardInterrupt:
        cleanup()
