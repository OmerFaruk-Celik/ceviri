#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import Gtk, AyatanaAppIndicator3

import os
import sys
import subprocess
import json
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sabitler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "ayarlar.json")
ICONS_DIR = os.path.join(BASE_DIR, "ICONS")

class CeviriGUI(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.celik.ceviri")
        self.window = None
        self.indicator = None
        self.ceviri_process = None

        # Varsayılan ayarlar
        self.from_lang = "en"
        self.to_lang = "tr"
        
        self.load_settings()

        # --- GÜNCELLENEN KISIM: Özel simge yolunu GTK'ya tanıtma ---
        self.icon_theme = Gtk.IconTheme.get_default()
        if os.path.isdir(ICONS_DIR):
            self.icon_theme.append_search_path(ICONS_DIR)
            logger.info(f"Özel simge yolu eklendi: {ICONS_DIR}")

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.create_app_indicator()
        self.create_main_window() # Pencereyi başlangıçta oluştur, gizli kalsın

    def do_activate(self):
        # Uygulama ikincil kez çalıştırıldığında ayar penceresini göster
        self.toggle_window(None)

    def create_main_window(self):
        self.window = Gtk.Window(application=self)
        self.window.set_title("Çeviri Ayarları")
        self.window.set_default_size(350, 200)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        # Pencere kapatıldığında yok olmasın, sadece gizlensin
        self.window.connect("delete-event", lambda w, e: w.hide() or True)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=15)
        self.window.add(vbox)

        lang_list = self.get_language_list()

        from_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        from_label = Gtk.Label(label="Kaynak Dil:")
        from_box.pack_start(from_label, False, False, 0)
        self.from_combo = Gtk.ComboBoxText()
        for code, name in lang_list:
            self.from_combo.append(code, name)
        self.from_combo.set_active_id(self.from_lang)
        from_box.pack_start(self.from_combo, True, True, 0)
        vbox.pack_start(from_box, False, False, 0)

        to_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        to_label = Gtk.Label(label="Hedef Dil:  ")
        to_box.pack_start(to_label, False, False, 0)
        self.to_combo = Gtk.ComboBoxText()
        for code, name in lang_list:
            self.to_combo.append(code, name)
        self.to_combo.set_active_id(self.to_lang)
        to_box.pack_start(self.to_combo, True, True, 0)
        vbox.pack_start(to_box, False, False, 0)

        save_btn = Gtk.Button(label="Kaydet ve Uygula")
        save_btn.connect("clicked", self.on_save_clicked)
        vbox.pack_start(save_btn, False, False, 10)

    def on_save_clicked(self, button):
        self.from_lang = self.from_combo.get_active_id()
        self.to_lang = self.to_combo.get_active_id()
        self.save_settings()
        logger.info(f"Ayarlar kaydedildi: from={self.from_lang}, to={self.to_lang}")
        
        # Eğer çeviri çalışıyorsa, yeni ayarlarla yeniden başlat
        if self.ceviri_process and self.ceviri_process.poll() is None:
            logger.info("Ayarlar değişti, çeviri yeniden başlatılıyor...")
            self.stop_ceviri()
            self.run_ceviri()

        self.window.hide()

    def create_icon_menu_item(self, label_text, icon_name, callback):
        item = Gtk.MenuItem()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_margin_start(5)
        # Simgeleri artık `new_from_icon_name` ile çağırıyoruz
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
        box.pack_start(image, False, False, 0)
        label = Gtk.Label(label=label_text, xalign=0)
        box.pack_start(label, True, True, 0)
        item.add(box)
        if callback:
            item.connect("activate", callback)
        item.show_all()
        return item

    def create_app_indicator(self):
        # Ana simge için .png uzantısı ile tam yolu belirtmek daha güvenli
        main_icon_path = os.path.join(ICONS_DIR, "images.png")
        if not os.path.exists(main_icon_path):
            main_icon_path = "dialog-information"

        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "ceviri-indicator", main_icon_path,
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()
        
        # --- GÜNCELLENEN KISIM: Menü öğeleri uzantısız simge adlarıyla çağrılıyor ---
        # Not: ICONS klasöründeki dosyalarınızın adı settings.png, start.png vb. olmalı.
        menu.append(self.create_icon_menu_item("Ayarlar", "settings", self.toggle_window))
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(self.create_icon_menu_item("Çeviriyi Başlat", "start", self.run_ceviri))
        menu.append(self.create_icon_menu_item("Çeviriyi Durdur", "stop", self.stop_ceviri))
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(self.create_icon_menu_item("Çıkış", "exit", self.do_quit))

        menu.show_all()
        self.indicator.set_menu(menu)

    def toggle_window(self, _):
        if not self.window.is_visible():
            self.window.show_all()
        self.window.present()

    def run_ceviri(self, _=None):
        if self.ceviri_process and self.ceviri_process.poll() is None:
            logger.info("Çeviri zaten çalışıyor.")
            return
        
        ceviri_script_path = os.path.join(BASE_DIR, "ceviri.py")
        if not os.path.exists(ceviri_script_path):
            logger.error(f"ceviri.py dosyası bulunamadı: {ceviri_script_path}")
            return
            
        cmd = [sys.executable, ceviri_script_path, self.from_lang, self.to_lang]
        logger.info(f"Çeviri başlatılıyor: {' '.join(cmd)}")
        self.ceviri_process = subprocess.Popen(cmd)

    def stop_ceviri(self, _=None):
        if self.ceviri_process and self.ceviri_process.poll() is None:
            logger.info("Çeviri durduruluyor.")
            # Ana süreci ve tüm alt süreçlerini sonlandır
            parent = psutil.Process(self.ceviri_process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            try:
                parent.wait(timeout=3)
            except psutil.TimeoutExpired:
                parent.kill()
            self.ceviri_process = None
        else:
            logger.info("Çeviri zaten çalışmıyor.")

    def do_quit(self, _=None):
        logger.info("Program kapatılıyor...")
        self.stop_ceviri()
        self.quit()

    def get_language_list(self):
        return [
            ("en", "İngilizce"),
            ("tr", "Türkçe"),
            ("de", "Almanca"),
            ("fr", "Fransızca"),
            ("es", "İspanyolca"),
            ("it", "İtalyanca"),
            ("ru", "Rusça"),
            ("zh-cn", "Çince (Basitleştirilmiş)"),
            ("ja", "Japonca"),
            ("ko", "Korece"),
            ("auto", "Otomatik Algıla"),
        ]

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            logger.info("Ayar dosyası bulunamadı, varsayılanlar kullanılacak.")
            return
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.from_lang = data.get("from_lang", self.from_lang)
                self.to_lang = data.get("to_lang", self.to_lang)
                logger.info("Ayarlar yüklendi.")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Ayarlar yüklenemedi: {e}")

    def save_settings(self):
        data = {"from_lang": self.from_lang, "to_lang": self.to_lang}
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("Ayarlar kaydedildi.")
        except IOError as e:
            logger.error(f"Ayarlar kaydedilemedi: {e}")

def main():
    # psutil kütüphanesini kontrol et, yoksa uyar
    try:
        import psutil
    except ImportError:
        print("HATA: 'psutil' kütüphanesi gerekli. Lütfen 'pip install psutil' komutu ile kurun.")
        sys.exit(1)
        
    app = CeviriGUI()
    sys.exit(app.run(sys.argv))

if __name__ == "__main__":
    main()
