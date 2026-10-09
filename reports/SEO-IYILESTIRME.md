# SEO iyileştirmesi — 9 Ekim 2026

248 bölge sayfasının 195'ine kaynaklı yer bilgisi eklendi: 30 ilçe, 144 mahalle ve 21 yol/tünel/sanayi. Valilik, belediye, İBB açık veri ve KGM kaynakları sayfalarda görünür bağlantılarla belirtilir. İlçeler için yer bilgisi, o konumda araç alınırken gerekli giriş, yön veya erişim bilgisine bağlanır. Bunlar işletmenin o bölgede yaptığı işin kanıtı değildir.

Alt sayfalara kopyalanan uzun ilçe paragrafları kaldırıldı. Eski siteden alınan doğrulanmamış yol listeleri yeni metinlerde kullanılmıyor. Liman Reis, belediye kaydı doğrultusunda Narlıdere ile ilişkilendirildi; mevcut URL korunarak kırık bağlantı oluşturulmadı. Semt adı ile resmî mahalle adı eşit kabul edilmedi.

53 bölge için yeterli resmî yer eşleştirmesi bulunamadı. Bu sayfalara tahminî sokak, tesis girişi veya çalışma örneği eklenmedi. Kapsam listesi `local-content-coverage.json` dosyasında. Bu sayfalar hâlâ daha fazla doğrulanmış bilgiye ihtiyaç duyuyor; tüm içerik açığı kapanmış sayılmaz. Belediye kaydının kontrol tarihi, her kaydın güncel saha durumu garantisi değildir.

262 içerik sayfası işletme sahibinin önceki talebi doğrultusunda index,follow ve sitemap kapsamında kalıyor. 404 kapsam dışında. Başlık/açıklama tekilliği, H1, canonical, JSON-LD, dahili bağlantı ve fragment, yönlendirme, tüm referans hedefleri ve sitemap doğrulamaları geçti.

## Mobil laboratuvar ölçümü

Lighthouse 12, yerel HTTP sunucusu, varsayılan mobil simülasyon ve boş önbellek kullanıldı. Ana sayfa önce/sonra aynı araç ve ayarlarla ölçüldü. Tam raporların ölçüm özeti `mobile-lighthouse.json` içinde.

| Ölçüm | Önce | Sonra |
|---|---:|---:|
| Ana sayfa performans | 89 | 99 |
| LCP | 3,5 sn | 1,8 sn |
| İlk içerik görünümü | 2,3 sn | 1,2 sn |
| CLS | 0,001 | 0 |
| Toplam aktarım | 448 KiB | 139 KiB |

Bornova sayfası: performans 100, LCP 1,7 sn, CLS 0. Erişilebilirlik, best-practices ve Lighthouse'ın sınırlı teknik SEO denetimi test edilen sayfalarda 100. Bu, tüm siteye SEO puanı veya Google sıralama garantisi değildir. Yerel sunucu ölçümü canlı hosting performansını ve gerçek ziyaretçi Core Web Vitals verisini göstermez.

Görseller WebP ve responsive srcset ile sunuluyor. Manrope fontları WOFF2'ye dönüştürüldü. Kritik kalın font önceden yükleniyor. CSS/JS sürümleri içerik özetiyle adreslenerek önceki tasarımın önbellekte kalması önleniyor. Onaylı renkler ve menü davranışı korunuyor.

## Yayın için kalan işler

`izmirotocekiciniz.com` DNS/SSL bağlantısı bekliyor. Mevcut Sites erişimi owner-private olduğundan Google'a açık yayın tamamlanmış değil. Alan adı sağlayıcısı/hosting bilgisi ve kullanıcı hesabındaki gerekli erişim olmadan DNS değişikliği veya Search Console doğrulaması yapılmadı. DNS kayıtları `launch/DNS-VE-YAYIN.md` dosyasında.

Yayın tamamlandığında canlı HTTPS, robots/sitemap, canonical ve 404 HTTP durumu kontrol edilmeli; ardından Search Console alan adı doğrulanıp sitemap gönderilmeli. Gerçek kullanım verisi oluşunca Core Web Vitals yeniden değerlendirilmeli. Eski site açık kalır; bu çalışmada eski siteye yönlendirme veya içerik değişikliği uygulanmadı.

İşletmeye ait gerçek çalışma örnekleri, kullanılan ekipmanın özellikleri ve yerel hizmet deneyimi ancak işletme sahibi doğruladığında eklenebilir. Uydurma yorum, şube, süre, fiyat veya sertifika eklenmedi.

İçerik yaklaşımı: [Google — Faydalı ve güvenilir içerik](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Kelime sayısı yerine doğrulanabilir bilgi ve kullanıcıya sağlanan fayda esas alındı.
