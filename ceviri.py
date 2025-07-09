import os
import sys
import subprocess
import threading
import psutil
import pyperclip
import pyautogui
from googletrans import Translator
from pynput import mouse
from pynput import keyboard as kb

# --- Yol ayarları bölümü ---
ev_dizini = os.path.expanduser("~")
github_dizini = os.path.join(ev_dizini, "github", "MAIN", "ceviri")
py_yol_dosyasi = os.path.join(github_dizini, "python")
try:
    with open(py_yol_dosyasi, "r") as f:
        surum = f.read()
    surum = surum.lower().strip()
    dizi = surum.split(".")
    if len(dizi) >= 2:
        surum = dizi[0] + "." + dizi[1]
        yol = os.path.join(github_dizini, 'VenvNotlar', 'lib', 'python' + surum, 'site-packages')
        sys.path.insert(0, yol)
except FileNotFoundError:
    print(f"Uyarı: Python sürüm dosyası bulunamadı: {py_yol_dosyasi}")
except Exception as e:
    print(f"Uyarı: Sanal ortam yolu ayarlanırken bir hata oluştu: {e}")
# --- Yol ayarları bitti ---

translator = Translator()
onceki_metin = ""
ceviri_aktif = True  # ALT+Q ile aç/kapat özelliği

def x(x1):
    with open("x", "w") as dosya:
        dosya.write(str(x1))

def y(y1):
    with open("y", "w") as dosya:
        dosya.write(str(y1))

def ekran_ortasi():
    ekran_genislik, ekran_yukseklik = pyautogui.size()
    x = ekran_genislik // 2
    y = ekran_yukseklik // 2
    return x, y




def kill_box_py():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'box.py' in proc.info['cmdline']:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def calistir():
    kill_box_py()  # Önce eski varsa kapat
    try:
        subprocess.Popen([sys.executable, 'box.py'])
        print("Box.py açıldı ve çalışıyor.")
    except Exception as e:
        print(f"box.py çalıştırılırken hata: {e}")



def metin(yazi):
    with open("metin", "w", encoding='utf-8') as dosya:
        dosya.write(yazi)

def perform_translation(kopyalanan_metin):
    global onceki_metin
    try:
        ceviri = translator.translate(kopyalanan_metin, src='en', dest='tr')

        if ceviri and ceviri.text and ceviri.text.strip() != onceki_metin:
            onceki_metin = ceviri.text.strip()
            print(f"Çeviri: {onceki_metin}")
            metin(onceki_metin)
            calistir()
    except Exception as e:
        print(f"Çeviri işlemi sırasında bir hata oluştu: {e}")

def on_click(x_coord, y_coord, button, pressed):
    if not pressed and button == mouse.Button.left:
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        kopyalanan_metin = pyperclip.paste()

        def islem_yap():
            if not ceviri_aktif:
                return
            koordinat = pyautogui.position()
            y(koordinat[1] - 120)
            x(koordinat[0] - 100)
            if kopyalanan_metin and kopyalanan_metin.strip():
                perform_translation(kopyalanan_metin)

        threading.Thread(target=islem_yap).start()

    return True

# --- ALT+Q tuş kombinasyonu kontrolü ---
pressed_keys = set()

def on_press(key):
    try:
        if key == kb.Key.alt_l or key == kb.Key.alt_r:
            pressed_keys.add("alt")
        elif hasattr(key, 'char') and key.char == 'q':
            if "alt" in pressed_keys:
                global ceviri_aktif
                ceviri_aktif = not ceviri_aktif
                durum = "aktif" if ceviri_aktif else "pasif"
                x1,y1=ekran_ortasi()
                x(x1)
                y(y1)
                metin(durum)
                calistir()
                print(f"Çeviri durumu: {durum}")
    except:
        pass

def on_release(key):
    if key == kb.Key.alt_l or key == kb.Key.alt_r:
        pressed_keys.discard("alt")

# Tuş dinleyiciyi başlat
kb.Listener(on_press=on_press, on_release=on_release).start()

# Ana program
print("Çeviri betiği başlatıldı. Çevirmek için metin seçip sol fare tuşunu bırakın.")
print("ALT+Q tuşuyla çeviriyi aç/kapat.")
print("Programdan çıkmak için terminalde CTRL+C tuşlarına basın.")

# Fare tıklama dinleyicisi
with mouse.Listener(on_click=on_click) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nProgram sonlandırıldı.")
