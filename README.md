🏛️ Sirâciyye: Modern Hanefi Miras Hesaplayıcı
Bu proje, Hanefi mezhebinin temel miras hukuku metni olan el-Ferâizü's-Sirâciyye kitabındaki kuralları temel alarak geliştirişmiş, modern arayüze sahip bir miras (ferâiz) hesaplama uygulamasıdır.

Python ve CustomTkinter kullanılarak geliştirilen bu uygulama; Hacb (mirastan düşürme), Avl, Red ve Asabe sıralaması gibi karmaşık İslam miras hukuku kurallarını otomatik olarak işler.

🌟 Özellikler
Modern ve Şık Arayüz: CustomTkinter ile hazırlanmış, göz yormayan koyu mod (Dark Mode) tasarımı.

Kolay Veri Girişi: Hata yapmayı önleyen "+ / -" butonlu sayaç sistemi.

Kapsamlı Varis Desteği:

Eşler: Karı, Koca.

Fürû (Alt Soy): Oğul, Kız, Oğlun Oğlu, Oğlun Kızı.

Usûl (Üst Soy): Baba, Anne, Dede (Baba Babası), Nineler (Anne ve Baba tarafı).

Havaşi (Yan Soy): Öz/Baba Bir/Anne Bir Kardeşler, Amcalar ve Amca Oğulları.

Akıllı Hesaplama Motoru:

Hacb (Engelleme): Kimin kimi mirastan düşürdüğünü otomatik algılar (Örn: Baba varken Dede'nin düşmesi).

Asabe Sıralaması: Kalan malı alacak erkek akrabaları fıkhi önceliğe göre (Oğul > Baba > Kardeş > Amca) tespit eder.

Ömeriyye (Gharrawayn): Eş, Anne ve Baba üçlüsünde Annenin "kalanın 1/3'ünü" alması kuralını uygular.

Nineler: Anne ve Baba tarafı ninelerin 1/6'yı ortaklaşa paylaşması durumunu çözer.

Avl ve Red: Payların paydayı aşması (Avl) veya artması (Red) durumlarını otomatik denkleştirir.

Detaylı Raporlama: Hesaplamanın sadece sonucunu değil, arkasındaki mantığı ve uygulanan kuralları (delilleriyle) adım adım gösterir.

Hassas Matematik: Fraction kütüphanesi kullanılarak ondalık hata payı olmadan kesirli (tam) hesaplama yapılır.

📸 Ekran Görüntüleri
(Buraya uygulamanın ekran görüntüsünü ekleyebilirsiniz. Örn: ![Arayüz](screenshot.png)) - Projeyi Github'a yükledikten sonra screenshots klasörüne bir resim atıp burayı güncelleyin.

🛠️ Kurulum
Projeyi bilgisayarınızda çalıştırmak için Python kurulu olmalıdır.

Repoyu Klonlayın:

Bash

git clone https://github.com/mtahaoztrk/hanefi-miras
cd hanefi-miras
Gerekli Kütüphaneyi Yükleyin: Proje, modern arayüz için customtkinter kullanır.

Bash

pip install customtkinter
Uygulamayı Çalıştırın:

Bash

python miras-uygulamasi.py
(Not: Dosya adınız modern_miras.py ise komutu ona göre düzenleyin)

🧠 Fıkhi Taban ve Algoritma
Bu yazılım, Sirâciyye metninde geçen şu kuralları uygular:

Ashab-ı Ferâiz: Kur'an-ı Kerim'de payları belirlenmiş varislerin (1/2, 1/4, 1/8, 2/3, 1/3, 1/6) hisselerini dağıtır.

Hacb-ı Hirman:

Oğul varken torunlar düşer.

Baba varken dede düşer.

Anne varken tüm nineler düşer.

Baba veya Oğul varken kardeşler düşer (Hanefi mezhebi görüşü).

Asabe: Ferâiz sahiplerinden artan malı alacak en yakın erkek akrabayı 4 sınıf kuralına göre bulur.

Oğul Kızı: Tek kız varken oğul kızının 2/3'ü tamamlamak için 1/6 alması (Tekmiletü's-sülüsân) kuralını işler.

🤝 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz:

Bu repoyu Fork'layın.

Yeni bir Branch oluşturun (git checkout -b ozellik/YeniOzellik).

Değişikliklerinizi Commit'leyin (git commit -m 'Yeni özellik eklendi').

Branch'inizi Push'layın (git push origin ozellik/YeniOzellik).

Bir Pull Request açın.

⚠️ Yasal Uyarı (Feragatname)
Bu yazılım eğitim ve yardımcı amaçlı geliştirilmiştir. Algoritma, Hanefi fıkhının temel metinlerine sadık kalmaya çalışsa da, karmaşık ve istisnai miras davalarında nihai hüküm için mutlaka uzman bir İslam hukukçusuna veya resmi makamlara danışılmalıdır. Yazılımın ürettiği sonuçların hukuki bağlayıcılığı yoktur.

📄 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.
