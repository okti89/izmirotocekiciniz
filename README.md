# İzmir Oto Çekiciniz

Hedef alan adı: https://izmirotocekiciniz.com
Telefon ve WhatsApp: +90 536 676 28 66. Çalışma saatleri: 7/24. Hedef hizmet alanı: İzmir’in 30 ilçesi.

262 içerik sayfası + 404. 248 tekil bölge sayfası: 30 ilçe, 189 mahalle/semt/diğer nokta, 21 güzergâh ve 8 sanayi sitesi. Sekiz hizmet sayfası ve yardımcı sayfalar korunur. Referanstaki 275 hedefin tamamı `url-mapping.json` içinde eşlenmiştir; aynı yerin farklı yazımları 301 ile tek içerik adresine gider. Eski sitede yönlendirme veya DNS değişikliği yapılmadı.

## Hazırlama ve doğrulama

`python3 build.py` özel önizlemeyi üretir. Tüm sayfalar noindex; canonical adresler hedef alan adını kullanır. Önizleme sitemap'i Google'a duyurulmaz.

`python3 tools/validate.py`

`python3 server.py` yerel önizlemeyi http://127.0.0.1:4173 üzerinde açar. Yerel sunucu, yönlendirmeleri ve gerçek 404 yanıtını da uygular.

## İlk kamuya açık yayın

`python3 build.py --public`

Bu işlem yalnızca ilk aşamadaki 16 sayfayı index yapar. Diğer 246 içerik sayfası noindex,follow kalır. İlk aşama sitemap'i `launch/sitemap.xml` dosyasında ayrıca hazırlanmıştır. Canonical, Open Graph, yapılandırılmış veri ve sitemap https://izmirotocekiciniz.com adresini kullanır.

DNS kaydı: `launch/DNS-VE-YAYIN.md`. Alan adı bağlantısı DNS/SSL doğrulaması bekliyor. Site erişimi halen sahibine özeldir; alan adı bağlanması bu ayarı değiştirmez. Kamuya açık erişim ve üretim çıktısı birlikte yayımlanmadan Search Console'a sitemap göndermeyin.

İlk aşama kontrolü: `python3 tools/validate.py --public`. Değişiklikten sonra özel önizlemeye dönmek için `python3 build.py` çalıştırın.

## Diğer sayfaların indekslenmesi

`index-regions.json` içindeki `indexable_paths` listesine yalnızca onaylanan canonical yolları ekleyin. Üretim derlemesi bunları sitemap'e ekler ve index etiketine geçirir. `publication-plan.json` mevcut aşamaları listeler.

Bölge sayfaları hizmet talebine yardımcı olan kısa rehberlerdir; başlık, gerçek ilçe ilişkisi, güzergâh/erişim bilgisi ve bölgeye özel WhatsApp talep bağlantısı içerir. Aynı mahalle adının birden fazla ilçede geçtiği durumlarda ilçe seçimi açıklanır. Ortak taşıma prosedürleri tekrar edebilir; yalnızca kelimeleri değiştirmek özgün yerel değer sayılmaz.

Kaynak yer bilgisi sınırlı olan sayfalarda özel ekip, şube, gerçek vaka, kesin süre veya fiyat uydurulmadı. İndeksleme genişletilmeden önce gerçek hizmet kayıtları, güncel erişim bilgileri ve varsa izinli operasyon örnekleriyle içerik incelenmelidir. Bütün sayfaların oluşturulması, bütün sayfaların Google tarafından indeksleneceği veya sıralanacağı anlamına gelmez.

`reference-facts.json` işletme sahibine ait referans siteden okunan yer bilgilerini; `region-catalog.json` birleşen adları ve yeni yolları saklar. Bu kaynak verileri operasyon iddialarını veya resmî coğrafi doğruluğu bağımsız olarak kanıtlamaz. Hatalı kaynak adres `/isikkoy-cekici`, Işıkkent sayfasına eşlenmiştir.

## Görseller ve işletme bilgisi

Görseller işletme sahibinin izniyle izmircekicioto.com'dan alındı. Ana görsel sıkıştırıldı; aşağıdaki galeri gecikmeli yüklenir. Görsellerden tarih, müşteri kimliği veya müdahale süresi türetilmedi. Sahte adres, yıldız ve yorum kullanılmadı. İşletme profili mevcutmuş gibi gösterilmez.

## Ölçüm ve SEO

Başlık, description, H1, canonical, JSON-LD, yerel bağlantılar, yönlendirme hedefleri, sitemap kapsamı ve indeksleme durumları kontrol edilir. Bunlar içerik kalitesi incelemesi veya sıralama garantisi değildir. Search Console gönderimi ve saha performans ölçümü henüz yapılmadı.

## Onaylanan tasarım ve içerik güncellemesi

Koyu lacivert, amber/sarı ve beyaz tasarım bütün sayfalarda kullanılır. Mobil hamburger menü sağdan kayar; Escape, arka plan ve kapatma düğmesiyle kapanır, klavye odağını korur. Ana sayfa, sekiz hizmet sayfası, Gaziemir, Menderes, fiyatlandırma ve hakkımızda içerikleri genişletildi. Hizmete özgü editoryal metinler content_enrichment.py dosyasında yönetilir. Diğer bölge sayfalarının ek yerel ve işletme kaynaklarıyla doğrulanması hâlâ gerekir; bu sayfalar varsayılan olarak noindex tutulur. Kelime sayısı veya sıralama garantisi verilmez.
