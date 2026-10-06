# İzmir Oto Çekiciniz

İlk aşama: 16 içerik sayfası ve bir 404 rotası. 8 özgün hizmet sayfası, Gaziemir ve Menderes bölge sayfaları; 30 ilçeyi ve referanstaki diğer hedefleri kapsayan aramalı rehber.

## Önizleme

`python3 build.py` tüm sayfalara noindex verir. Özel önizleme sitemap'i boş tutulur. Sahte adres, şube, yıldız veya müşteri yorumu bulunmaz. Telefon/WhatsApp: +90 536 676 28 66; çalışma saatleri 7/24.

`python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`

## Asıl alan adına geçiş

`python3 build.py --public --origin https://GERCEK-ALAN-ADI`

Bu komut 16 hazır içerik sayfasını indekslenebilir yapar ve yalnızca bu URL'leri sitemap'e ekler. Önce gerçek alan adını seçin; iki siteyi eşdeğer içerikle indekslemeye açmayın. Mevcut alan adının yerini alacaksa eski URL'ler için sayfa bazında 301 eşlemesi hazırlayın; eski SEO değeri olan bölge sayfalarını otomatik olarak kaldırmayın. Farklı markalı yeni alan adıysa içerik ve işletme ilişkisini ayrıca değerlendirin. Yönlendirmeler ve DNS henüz uygulanmadı.

`content-backlog.json` tüm kalan referans hedeflerini içerir. Kalan hedefler yayınlanmış bağımsız sayfalar değildir. İlçe/mahalle/güzergâh adının değişmesi bir sayfayı özgün yapmaz; doğrulanmış yerel fayda sağlandıktan sonra sayfa ekleyin.

Her yayın öncesi: gerçek hizmet kapsamı, iletişim, robots/noindex ve canonical alan adı, sitemap, iç bağlantılar ve görsel erişimi kontrol edilmeli. Search Console gönderimi için alan adı doğrulaması gerekir. Performans saha verileri henüz mevcut değildir.

## Görseller

İşletme sahibinin izniyle izmircekicioto.com'dan alındı. Açılış görseli sıkıştırıldı; galeri aşağıda gecikmeli yüklenir. Görsellerden iş tarihi, müdahale süresi veya müşteri referansı çıkarılmadı.

## Google İşletme Profili

Çekici olmak tek başına profil oluşturmayı engellemez. Müşterinin bulunduğu yere giden işletmeler hizmet bölgesi modeli kapsamında değerlendirilebilir. Gerçek adres/işletme bilgileriyle uygunluk ve doğrulama ayrıca yapılmalı. Kaynak: https://support.google.com/business/answer/9157481?hl=tr
