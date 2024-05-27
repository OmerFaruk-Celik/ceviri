from pynput import mouse
import pyautogui
from googletrans import Translator
import subprocess
import pyperclip

import sys

#belgeler isimli klasörüne gidiyor
import os

# Ev dizinini al
ev_dizini = os.path.expanduser("~")

# Github dizinini birleştir
github_dizini = os.path.join(ev_dizini, "github","MAIN","ceviri")

# NotDefteri dizinini birleştir
py_yol = os.path.join(github_dizini,"python")

with open(py_yol, "r") as f:
	surum=f.read()
surum=surum.lower()
surum=surum.replace(" ","")
dizi=surum.split(".")
surum=dizi[0]+"."+dizi[1]
yol=	github_dizini+'/VenvNotlar/lib/'+surum+'/site-packages'
sys.path.insert(0, yol) 

translator = Translator()
onceki_metin = ""

def x(x1):
    with open("x", "w") as dosya:
        dosya.write(str(x1))

def y(y1):
    with open("y", "w") as dosya:
        dosya.write(str(y1))

def calistir():
    # box.py dosyasını çalıştır
    process = subprocess.Popen(['python', 'box.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    #print(error)


def metin(metin):
    with open("metin", "w") as dosya:
        dosya.write(metin)
    return metin

def on_click(x1, y1, button, pressed):
    global onceki_metin
    if not pressed and button == mouse.Button.left:

        pyautogui.hotkey('ctrl', 'c')
        koordinat = pyautogui.position()

        x1 = koordinat[0]
        y1 = koordinat[1]
        y(y1 - 120)
        x(x1 - 100)

        # Kopyalanan metni al
        kopyalanan_metin = pyperclip.paste()
        
        if kopyalanan_metin:
            ceviri = translator.translate(kopyalanan_metin, src='en', dest='tr')

            if ceviri.text != onceki_metin:
                onceki_metin = ceviri.text
                metin(ceviri.text)
                #print(len(ceviri.text)*5)
                #print(ceviri.text)
                calistir()

    return True

# Fare olaylarını dinle
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
