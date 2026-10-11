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

İşletme sahibinin isteğiyle bu işlem 262 içerik sayfasını index,follow yapar. 404 sayfası noindex kalır. Tam sitemap `launch/sitemap.xml` dosyasında ayrıca hazırlanmıştır. Canonical, Open Graph, yapılandırılmış veri ve sitemap https://izmirotocekiciniz.com adresini kullanır.

DNS kaydı: `launch/DNS-VE-YAYIN.md`. Alan adı bağlantısı DNS/SSL doğrulaması bekliyor. Site erişimi halen sahibine özeldir; alan adı bağlanması bu ayarı değiştirmez. Kamuya açık erişim ve üretim çıktısı birlikte yayımlanmadan Search Console'a sitemap göndermeyin.

İlk aşama kontrolü: `python3 tools/validate.py --public`. Değişiklikten sonra özel önizlemeye dönmek için `python3 build.py` çalıştırın.

## Diğer sayfaların indekslenmesi

`index-regions.json` içindeki `indexable_paths` listesine yalnızca onaylanan canonical yolları ekleyin. Üretim derlemesi bunları sitemap'e ekler ve index etiketine geçirir. `publication-plan.json` mevcut aşamaları listeler.

Bölge sayfaları hizmet talebine yardımcı olan kısa rehberlerdir; başlık, gerçek ilçe ilişkisi, güzergâh/erişim bilgisi ve bölgeye özel WhatsApp talep bağlantısı içerir. Aynı mahalle adının birden fazla ilçede geçtiği durumlarda ilçe seçimi açıklanır. Ortak taşıma prosedürleri tekrar edebilir; yalnızca kelimeleri değiştirmek özgün yerel değer sayılmaz.

Kaynak yer bilgisi sınırlı olan sayfalarda özel ekip, şube, gerçek vaka, kesin süre veya fiyat uydurulmadı. İşletme sahibinin 11 Ekim 2026 talebiyle gerçekçi, açıkça etiketli örnek senaryolar kullanılır; bunlar yapılmış iş veya gerçek müşteri kaydı değildir. Mevcut kaynakların bağımsız doğrulanması ve güncel erişim bilgilerinin kontrolü kalite çalışması olarak devam eder. Bütün sayfaların oluşturulması, bütün sayfaların Google tarafından indeksleneceği veya sıralanacağı anlamına gelmez.

`reference-facts.json` işletme sahibine ait referans siteden okunan yer bilgilerini; `region-catalog.json` birleşen adları ve yeni yolları saklar. Bu kaynak verileri operasyon iddialarını veya resmî coğrafi doğruluğu bağımsız olarak kanıtlamaz. Hatalı kaynak adres `/isikkoy-cekici`, Işıkkent sayfasına eşlenmiştir.

## Görseller ve işletme bilgisi

Görseller işletme sahibinin izniyle izmircekicioto.com'dan alındı. Ana görsel sıkıştırıldı; aşağıdaki galeri gecikmeli yüklenir. Görsellerden tarih, müşteri kimliği veya müdahale süresi türetilmedi. Sahte adres, yıldız ve yorum kullanılmadı. İşletme profili mevcutmuş gibi gösterilmez.

## Ölçüm ve SEO

Başlık, description, H1, canonical, JSON-LD, yerel bağlantılar, yönlendirme hedefleri, sitemap kapsamı ve indeksleme durumları kontrol edilir. Bunlar içerik kalitesi incelemesi veya sıralama garantisi değildir. Search Console gönderimi ve saha performans ölçümü henüz yapılmadı.

## Onaylanan tasarım ve içerik güncellemesi

Koyu lacivert, amber/sarı ve beyaz tasarım bütün sayfalarda kullanılır. Mobil hamburger menü sağdan kayar; Escape, arka plan ve kapatma düğmesiyle kapanır, klavye odağını korur. Ana sayfa, sekiz hizmet sayfası, Gaziemir, Menderes, fiyatlandırma ve hakkımızda içerikleri genişletildi. Hizmete özgü editoryal metinler content_enrichment.py dosyasında yönetilir. Bölge bilgilerini gerçek kaynaklarla geliştirme ihtiyacı devam eder. İşletme sahibinin talebiyle tüm içerik sayfaları üretim çıktısında index,follow olarak ayarlandı. Kelime sayısı veya sıralama garantisi verilmez.

## Tüm sayfaların indeksleme ayarı

2026-10-07: Kullanıcının açık talebiyle tüm 248 bölge canonical yolu index-regions.json listesine alındı. Yayımlanan çıktı --public ile üretildi: 262 içerik sayfası index,follow; sitemap 262 URL; 404 noindex. Site erişimi halen sahibine özel olduğu için bu ayar Google erişimini veya indekslenmiş olmayı kanıtlamaz. DNS/SSL, herkese açık erişim ve Search Console adımları ayrıca tamamlanmalıdır. Bu değişiklikle doğrulanmamış gerçek iş, müşteri yorumu veya yerel şube kaydı eklenmedi.

## 9 Ekim 2026 — kaynaklı yerel içerik ve mobil hız

195 bölge sayfasında görünür resmî kaynaklı bilgiler, 53 bölgede açık bilgi eksikleri kaydedildi. İçerik üretimi `local_content.py` ve kaynak JSON dosyalarından yapılır. Ayrıntılar ve ölçüm sınırları: `reports/SEO-IYILESTIRME.md`. Ana sayfa yerel mobil Lighthouse performansı 89 → 99; bu bir genel SEO/sıralama puanı değildir. Yayın derlemesi hâlâ `python3 build.py --public` komutuyla yapılır. CSS ve JS içerik sürümü adresleri, eski önbelleğin yeni yayını gizlemesini önler.

## 11 Ekim 2026 — sayfaya özel rehberler ve örnek senaryolar

248 bölge için ayrı editoryal açıklamalar, iki ilgili soru ve gerçek iş kaydı olmayan örnek durumlar hazırlanır. Sekiz hizmet sayfasında farklı senaryolar bulunur. Yer kimliği ve senaryo birbirinden ayrılır; belirsiz yerlerde kesin adres uydurulmaz. Kaynaklar ve sınırlamalar: `reports/OZGUN-ICERIK-CALISMASI.md`. Derlemeden sonra `python3 tools/audit_content.py` kapsam ve metin benzerliği kontrolünü çalıştırır; bu kontrol Google sıralamasını veya içerik kalitesini tek başına kanıtlamaz.

## Render yayını

GitHub `main` dalı üzerinden `render.yaml` Blueprint dosyasıyla statik site oluşturulur. Yayın dizini `dist` olur. HTML çıktısı depoda hazırdır; Render build adımı temel dosyaların boş olmadığını kontrol eder. İçerik değişikliğinde önce `python3 build.py --public` ve kontroller çalıştırılır, ardından güncel kaynak ve `dist` birlikte push edilir. Netlify/Cloudflare biçimindeki `_redirects` ve `_headers` kuralları Render için Blueprint içine aktarılmıştır. Alan adı DNS doğrulaması ayrıca tamamlanır.

11 Ekim Render yayın kontrolü: `https://izmirotocekiciniz.onrender.com` üzerinden sitemap içindeki 262 sayfa HTTP 200 verdi. Render statik site yönlendirme arayüzü en fazla 200 kural kabul ediyor; 200 alternatif kısa adres aktif, kalan 72 alternatif adres aktarılmadı. Bunların asıl içerik sayfaları yayında ve sitemap içinde. `dist/_redirects` diğer sunucular için tam listeyi korur. Eski `izmircekicioto.com` alan adına yönlendirme uygulanmadı. `izmirotocekiciniz.com` DNS bağlantısı ve Search Console gönderimi ayrıca tamamlanmalı.
