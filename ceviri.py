import os
import sys
import threading
import time
import pyperclip
import pyautogui
import psutil
from pynput import mouse, keyboard
from googletrans import Translator
import json

# Ayarlar dosyası
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "ayarlar.json")

def load_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Default diller
        return {"from_lang": "tr", "to_lang": "en"}

settings = load_settings()
translator = Translator()

g_current_box_process = None
g_process_lock = threading.Lock()
g_latest_job_id = 0
g_job_id_lock = threading.Lock()
g_previous_clipboard = ""
ceviri_aktif = True

def write_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(content))

def ekran_ortasi():
    w, h = pyautogui.size()
    return w // 2, h // 2

def launch_box(text_to_show, x_pos, y_pos):
    global g_current_box_process
    with g_process_lock:
        if g_current_box_process and psutil.pid_exists(g_current_box_process.pid):
            try:
                psutil.Process(g_current_box_process.pid).kill()
            except psutil.NoSuchProcess:
                pass
        
        write_to_file("metin", text_to_show)
        write_to_file("x", x_pos - 100)
        write_to_file("y", y_pos - 120)

        g_current_box_process = None
        # box.py'yi başlat (aynı dizinde)
        import subprocess
        try:
            g_current_box_process = subprocess.Popen([sys.executable, "box.py"],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"box.py başlatılamadı: {e}")
            g_current_box_process = None

def perform_translation(kopyalanan_metin, x_pos, y_pos, job_id):
    try:
        ceviri = translator.translate(kopyalanan_metin, 
                                     src=settings.get("from_lang", "tr"),
                                     dest=settings.get("to_lang", "en"))
        text_sonuc = ceviri.text.strip() if (ceviri and ceviri.text) else None

        with g_job_id_lock:
            if job_id != g_latest_job_id:
                return  # Daha yeni iş var iptal

        if text_sonuc:
            print(f"Çeviri (#{job_id}): {text_sonuc}")
            launch_box(text_sonuc, x_pos, y_pos)

    except Exception as e:
        print(f"Çeviri hatası: {e}")

def on_click(x, y, button, pressed):
    global g_latest_job_id, g_previous_clipboard
    if not pressed and button == mouse.Button.left and ceviri_aktif:
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)

        kopyalanan_metin = pyperclip.paste()
        kopyalanan_metin_temiz = kopyalanan_metin.strip() if kopyalanan_metin else ""

        if kopyalanan_metin_temiz and kopyalanan_metin_temiz != g_previous_clipboard:
            g_previous_clipboard = kopyalanan_metin_temiz
            with g_job_id_lock:
                g_latest_job_id += 1
                current_job_id = g_latest_job_id
            
            print(f"Yeni seçim algılandı (#{current_job_id}): '{kopyalanan_metin_temiz[:30]}...'")
            threading.Thread(target=perform_translation,
                             args=(kopyalanan_metin_temiz, x, y, current_job_id)).start()

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
    except AttributeError:
        pass

def on_release(key):
    try:
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            pressed_keys.discard("Alt")
    except AttributeError:
        pass

def cleanup():
    print("\nTemizlik yapılıyor...")
    global g_current_box_process
    if g_current_box_process and psutil.pid_exists(g_current_box_process.pid):
        psutil.Process(g_current_box_process.pid).kill()
    print("Program sonlandırıldı.")

if __name__ == "__main__":
    pyperclip.copy("")
    g_previous_clipboard = ""

    from pynput import keyboard, mouse
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    print("Çeviri betiği başlatıldı.")
    print("-> Metin seçin ve sol tıklamayı bırakın.")
    print("-> ALT+Q ile çeviri modunu aç/kapatabilirsiniz.")
    print("-> Programdan çıkmak için CTRL+C basın.")

    try:
        keyboard_listener.join()
    except KeyboardInterrupt:
        cleanup()
