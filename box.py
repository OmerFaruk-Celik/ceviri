import tkinter as tk

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
