🚀 Anlık Çeviri Asistanı

![alt text](./ICONS/images.png)

Anlık Çeviri Asistanı, Ubuntu masaüstü için geliştirilmiş, seçtiğiniz herhangi bir metni anında çeviren pratik bir araçtır. Arka planda sessizce çalışır, sistem kaynaklarını verimli kullanır ve paneldeki simgesi üzerinden kolayca yönetilir.
✨ Ana Özellikler

    Anında Çeviri: Bir metni fare ile seçip bıraktığınızda otomatik olarak çevirir.

    Kolay Kontrol: Paneldeki simgesinden çeviriyi başlatın, durdurun veya ayarlara erişin.

    Kişiselleştirilebilir Dil Seçimi: Kullanıcı dostu arayüzden kaynak ve hedef dilleri kolayca değiştirin.

    Sistem Entegrasyonu: Ubuntu paneli ile tam uyumlu çalışır ve sistem başlangıcında otomatik olarak başlar.

📸 Ekran Görüntüleri

Uygulamanın şık ve kullanışlı arayüzü.

Panel Menüsü:
<p align="center">
<img src="https://raw.githubusercontent.com/OmerFaruk-Celik/ceviri/main/ICONS/start.png" alt="Başlat" width="24"/> Başlat &nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/OmerFaruk-Celik/ceviri/main/ICONS/stop.png" alt="Durdur" width="24"/> Durdur &nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/OmerFaruk-Celik/ceviri/main/ICONS/settings.png" alt="Ayarlar" width="24"/> Ayarlar &nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/OmerFaruk-Celik/ceviri/main/ICONS/exit.png" alt="Çıkış" width="24"/> Çıkış
</p>
*(Not: Menünün ve ayar penceresinin gerçek ekran görüntülerini buraya eklemek projeyi daha çekici kılacaktır.)*
🛠️ Ubuntu 22.04 için Kurulum

Kurulum süreci, tek bir betik ile tüm bağımlılıkları ve ayarları otomatik olarak yapar.
Adım 1: Projeyi İndirin

Terminali açın ve projeyi bilgisayarınıza klonlayın.
Generated bash

      
    git clone https://github.com/OmerFaruk-Celik/ceviri.git
    cd ceviri/

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END
Adım 2: Kurulum Betiğini Çalıştırın

Aşağıdaki komutlarla kurulumu başlatın. Betik, sistem dosyalarını kurmak için yönetici izni (sudo şifresi) isteyecektir.
Generated bash

      
    chmod +x INSTALL
    ./INSTALL

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Bu betik aşağıdaki işlemleri otomatik olarak yapar:

    Gerekli sistem kütüphanelerini (GTK, AppIndicator vb.) kurar.

    venv adında bir Python sanal ortamı oluşturur.

    Gerekli Python paketlerini (requirements.txt içindekiler) sanal ortama yükler.

    Uygulamalar menüsü için bir kısayol oluşturur.

    Sistemin her başlangıcında uygulamanın otomatik çalışması için ayar yapar.

Adım 3: Uygulamayı Başlatın

Kurulum tamamlandığında, Ubuntu'nun Uygulamalar menüsünden "Anlık Çeviri Asistanı" diye aratarak programı başlatabilirsiniz. Panelinizin sağ üst köşesinde uygulama simgesi belirecektir.

Eğer simge hemen görünmezse, lütfen oturumunuzu kapatıp yeniden açın.
🚀 Nasıl Kullanılır?

    Başlatın: Uygulama, kurulum sonrası sistem her açıldığında otomatik olarak başlar.

    Dil Ayarlayın: Paneldeki simgeye tıklayıp Ayarlar menüsünden dilleri seçin ve kaydedin.

    Çeviri Yapın: Herhangi bir metni fare ile seçip bıraktığınızda çeviri otomatik olarak ekranda belirir.

    Kontrol Edin: Paneldeki menüden çeviriyi geçici olarak durdurabilir veya yeniden başlatabilirsiniz.

💻 Geliştirme

Projeye katkıda bulunmak veya yerel geliştirme ortamı kurmak için:

Gerekli Sistem Paketleri:
Generated bash

          
    sudo apt update
    sudo apt install -y python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0 libayatana-appindicator3-dev

        

GNORE_WHEN_COPYING_START

Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Sanal Ortam ve Bağımlılıklar:
Generated bash

      
# Proje klasöründeyken
    python3 -m venv --system-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

    

IGNORE_WHEN_COPYING_START

Use code with caution. Bash
IGNORE_WHEN_COPYING_END

--system-site-packages bayrağı, PyGObject'in sistem versiyonunu kullanarak derleme sorunlarını önler.

requirements.txt İçeriği

Projenin ihtiyaç duyduğu Python paketleri:
Generated code

      
    pyperclip
    pyautogui
    googletrans==4.0.0-rc1
    pynput
    psutil
    PyGObject

    

IGNORE_WHEN_COPYING_START
Use code with caution.
IGNORE_WHEN_COPYING_END
🤝 Katkıda Bulunma

Her türlü katkı ve geri bildirim, projeyi daha iyi hale getirecektir. Bir "pull request" açmaktan veya "issue" oluşturmaktan çekinmeyin.
📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.
