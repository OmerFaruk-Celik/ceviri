import tkinter as tk
import sys
import os

ev_dizini = os.path.expanduser("~")
github_dizini = os.path.join(ev_dizini, "github", "MAIN", "ceviri")
py_yol = os.path.join(github_dizini, "python")

with open(py_yol, "r") as f:
    surum = f.read().strip().lower().replace(" ", "")
dizi = surum.split(".")
surum = dizi[0] + "." + dizi[1]
yol = os.path.join(github_dizini, 'VenvNotlar', 'lib', surum, 'site-packages')
sys.path.insert(0, yol)

def close_window():
    if root.winfo_exists():
        root.destroy()
        print("Pencere kapatıldı.")

def x():
    with open("x", "r") as dosya:
        return dosya.read()

def y():
    with open("y", "r") as dosya:
        return dosya.read()

def metin():
    with open("metin", "r") as dosya:
        return dosya.read()

root = tk.Tk()
root.geometry(f"100x50+{x()}+{y()}")
root.title("Çeviri")

label = tk.Label(root, text=metin(), font=("Arial", 12), fg="blue")
label.pack()

def update_metin():
    label.config(text=metin())
    uzunluk = len(metin())
    x_piksel = max(200, min(uzunluk * 10, 1900))
    root.geometry(f"{x_piksel}x50+{x()}+{y()}")
    root.after(100, update_metin)

button = tk.Button(root, text="Kapat", command=close_window)
button.pack(side=tk.BOTTOM)

# Otomatik kapanma
root.after(2100, close_window)

# İlk güncelleme
update_metin()
print("Box.py açıldı ve çalışıyor.")
root.mainloop()
import sys
sys.exit(0)
