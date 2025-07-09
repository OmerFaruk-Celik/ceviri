import tkinter as tk
from tkinter import ttk
import sys
import os

# --- Sabitler ve Ayarlar ---
MIN_WIDTH = 120       # Minimum pencere genişliği
MIN_HEIGHT = 60       # Minimum pencere yüksekliği
MAX_WIDTH = 600       # Maksimum pencere genişliği
MAX_HEIGHT = 400      # Maksimum pencere yüksekliği
PADDING = 15          # Kenar boşluğu

# --- Dinamik Kapanma Süresi Hesaplama ---
def calculate_timeout(text):
    word_count = len(text.split())
    calculated_ms = word_count * 300
    timeout_ms = max(2000, min(calculated_ms, 30000))
    print(f"box.py: {word_count} kelime için {timeout_ms}ms bekleme süresi ayarlandı.")
    return timeout_ms

# --- Dosya Okuma Fonksiyonu ---
def read_file_safely(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

# --- Ana Pencere ve Widget'lar ---
root = tk.Tk()
root.title("Çeviri")
root.attributes('-topmost', True)

def close_window(event=None):
    if root.winfo_exists():
        root.destroy()

style = ttk.Style(root)
style.configure("TFrame", background="#f0f0f0")
style.configure("TButton", padding=5)

main_frame = ttk.Frame(root, padding=PADDING)
main_frame.pack(fill=tk.BOTH, expand=True)

text_frame = ttk.Frame(main_frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
text_widget = tk.Text(
    text_frame, wrap=tk.WORD, font=("Arial", 12),
    fg="#000050", bg="#f0f0f0", relief=tk.FLAT,
    yscrollcommand=scrollbar.set
)
scrollbar.config(command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

close_button = ttk.Button(main_frame, text="Kapat", command=close_window)
close_button.pack(side=tk.BOTTOM, pady=(10, 0))

root.bind('<Escape>', close_window)

# --- İçeriği Ekle ---
translated_text = read_file_safely("metin")
text_widget.insert(tk.END, translated_text)
text_widget.config(state=tk.DISABLED)

# --- Dinamik Boyut Hesaplama ---
root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
root.update_idletasks()

lines = translated_text.split('\n')
max_line_length = max((len(line) for line in lines), default=1)
line_count = len(lines)

char_width_px = 7.5    # Arial 12 font için yaklaşık genişlik
line_height_px = 20    # Satır yüksekliği yaklaşık

ideal_width = int(max_line_length * char_width_px) + scrollbar.winfo_reqwidth() + (PADDING * 2)
ideal_height = int(line_count * line_height_px) + close_button.winfo_reqheight() + (PADDING * 3)

final_width = int(max(MIN_WIDTH, min(ideal_width, MAX_WIDTH)))
final_height = int(max(MIN_HEIGHT, min(ideal_height, MAX_HEIGHT)))

# --- Koordinat Ayarı ---
try:
    start_x = int(read_file_safely("x"))
    start_y = int(read_file_safely("y"))
except (ValueError, TypeError):
    print("box.py: Koordinat dosyaları okunamadı, varsayılan konum kullanılıyor.")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    start_x = (screen_width // 2) - (final_width // 2)
    start_y = (screen_height // 2) - (final_height // 2)

# --- Pencere Konumlandırma ---
root.geometry(f"{final_width}x{final_height}+{start_x}+{start_y}")
root.focus_force()

print(f"box.py: Pencere boyutu {final_width}x{final_height} olarak ayarlandı.")

# --- Otomatik Kapanma ---
timeout = calculate_timeout(translated_text)
root.after(timeout, close_window)

root.mainloop()
sys.exit(0)
