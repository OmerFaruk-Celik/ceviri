🚀 Anlık Çeviri Uygulaması

![alt text](./ICONS/images.png)

Anlık Çeviri, Ubuntu için geliştirilmiş, seçtiğiniz metni anında istediğiniz dile çeviren ve ekranınızda bir bildirim kutusuyla gösteren pratik bir masaüstü uygulamasıdır. Arka planda çalışır, sistem kaynaklarını verimli kullanır ve paneldeki simgesi üzerinden kolayca yönetilebilir.

Metin seçin, bırakın ve çevirisi anında karşınızda!
✨ Özellikler

    Anında Çeviri: Bir metni fare ile seçip bıraktığınızda otomatik olarak çevirir.

    Ayar Menüsü: Kaynak ve hedef dilleri kolayca değiştirmenizi sağlayan kullanıcı dostu bir ayar penceresi.

    Sistem Tepsisi (Tray) Entegrasyonu: Uygulama, Ubuntu panelinde bir simge olarak yaşar.

    Kolay Kontrol: Tek tıkla çeviriyi başlatın, durdurun veya ayarlara erişin.

    Kişiselleştirilebilir: Desteklenen diller listesinden istediğiniz kombinasyonu seçin.

    Otomatik Başlatma (Opsiyonel): INSTALL betiği ile sistemi her başlattığınızda otomatik olarak çalışacak şekilde ayarlanabilir.

📸 Ekran Görüntüleri

Uygulamanın şık ve kullanışlı arayüzü.

Paneldeki Uygulama Menüsü:
Tüm kontrollere buradan erişebilirsiniz.
<p align="center">
<img src="./ICONS/start.png" alt="Başlat" width="32"/>
<img src="./ICONS/stop.png" alt="Durdur" width="32"/>
<img src="./ICONS/settings.png" alt="Ayarlar" width="32"/>
<img src="./ICONS/exit.png" alt="Çıkış" width="32"/>
</p>
*(Not: Bu kısma uygulamanın menüsünün gerçek bir ekran görüntüsünü eklerseniz daha da güzel durur.)*

Ayar Penceresi:
Kaynak ve hedef dilleri bu pencereden kolayca seçin.
(Not: Bu kısma ayar penceresinin gerçek bir ekran görüntüsünü ekleyin.)
🛠️ Ubuntu 22.04 için Kurulum Adımları

Uygulamayı sisteminize kurmak ve çalıştırmak için aşağıdaki adımları takip edebilirsiniz. Kurulum, gerekli tüm bağımlılıkları otomatik olarak yükleyecektir.
Adım 1: Projeyi Klonlama

Öncelikle, projeyi bilgisayarınıza indirin. Terminali açın ve aşağıdaki komutu çalıştırın:
Generated bash

      
git clone https://github.com/KULLANICI_ADINIZ/PROJE_ADINIZ.git
cd PROJE_ADINIZ/

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

(KULLANICI_ADINIZ/PROJE_ADINIZ kısmını kendi GitHub bilgilerinizle güncellemeyi unutmayın.)
Adım 2: Kurulum Betiğini Çalıştırma

Proje klasörünün içindeyken, INSTALL betiğini çalıştırma izni verin ve çalıştırın. Bu betik, gerekli sistem kütüphanelerini kuracak, Python sanal ortamını oluşturacak ve uygulama kısayolunu yaratacaktır.
Generated bash

      
chmod +x INSTALL
./INSTALL

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Kurulum sırasında sizden yönetici (sudo) şifreniz istenebilir.
Adım 3: Uygulamayı Başlatma

Kurulum tamamlandıktan sonra, Ubuntu'nun "Uygulamalar" menüsünü açıp "Anlık Çeviri" (veya belirlediğiniz başka bir isim) diye aratarak uygulamayı bulabilir ve başlatabilirsiniz.

Uygulama başlatıldığında, ekranınızın sağ üst köşesindeki panelde simgesini göreceksiniz.
🚀 Kullanım

    Uygulamayı Başlatın: Uygulamalar menüsünden veya terminalden çalıştırın.

    Ayarları Yapılandırın (İsteğe Bağlı): Paneldeki simgeye tıklayıp "Ayarlar" menüsünü seçin. Kaynak ve hedef dilleri belirleyip "Kaydet" butonuna tıklayın.

    Çeviriyi Başlatın: Menüden "Çeviriyi Başlat" seçeneğine tıklayın.

    Çeviri Yapın: Herhangi bir yerde bir metin seçin (örneğin bir web sayfasında veya PDF belgesinde). Fare tuşunu bıraktığınız anda seçili metin çevrilecek ve ekranınızda belirecektir.

    Durdurma: Çeviri işlemini geçici olarak durdurmak için menüden "Çeviriyi Durdur" seçeneğini kullanabilirsiniz.

💻 Geliştirme

Bu proje Python ve GTK kullanılarak geliştirilmiştir. Geliştirme ortamını kurmak için:

    Projeyi klonlayın (Adım 1'deki gibi).

    Gerekli sistem geliştirme kütüphanelerini kurun:
    Generated bash

          
    sudo apt update
    sudo apt install -y python3-venv python3-dev libayatana-appindicator3-dev libgirepository1.0-dev build-essential libcairo2-dev pkg-config

        

    IGNORE_WHEN_COPYING_START

Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Bir sanal ortam oluşturun ve aktive edin:
Generated bash

      
python3 -m venv venv
source venv/bin/activate

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Gerekli Python paketlerini yükleyin:
Generated bash

      
pip install -r requirements.txt

    

IGNORE_WHEN_COPYING_START

    Use code with caution. Bash
    IGNORE_WHEN_COPYING_END

    Not: requirements.txt dosyanızda şu paketler olmalıdır: PyGObject, psutil, pynput, pyautogui, pyperclip, googletrans==4.0.0-rc1

🤝 Katkıda Bulunma

Katkılarınız projeyi daha da ileriye taşıyacaktır! Lütfen bir "pull request" açmaktan veya "issue" oluşturmaktan çekinmeyin.
📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.
