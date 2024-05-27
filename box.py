import tkinter as tk
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

def close_window():
    root.destroy()

def x():
    with open("x", "r") as dosya:
        x = dosya.read()
    return x

def y():
    with open("y", "r") as dosya:
        y = dosya.read()
    return y

def metin():
    with open("metin", "r") as dosya:
        metin = dosya.read()
    return metin

root = tk.Tk()
root.geometry(f"100x50+{x()}+{y()}")
root.title("Çeviri")
label = tk.Label(root, text=metin(), font=("Arial", 12), fg="blue")
label.pack()

def calistir():
    root.after(100, update_metin)

def update_metin():
    label.config(text=metin())
    
    letter_length = len(metin())
    x_piksel = letter_length * 10
    if x_piksel < 200:
        x_piksel = 200
    elif x_piksel > 1900:
        x_piksel = 1900
    root.geometry(f"{x_piksel}x50+{x()}+{y()}")
    root.after(100, update_metin)

button = tk.Button(root, text="Kapat", command=close_window)
button.pack(side=tk.BOTTOM)

calistir()
root.mainloop()
