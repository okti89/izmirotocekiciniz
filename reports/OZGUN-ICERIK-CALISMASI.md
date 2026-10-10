# Sayfaya özel içerik çalışması — 11 Ekim 2026

Amaç, aynı metinde yalnızca yer adı değiştirmek yerine her sayfanın ana açıklamasını, kullanım odağını, sorularını ve örnek durumunu ayrı hazırlamaktır. Menü, iletişim, kaynak notları, tabloların sütun başlıkları ve ortak hizmet bağlantıları aynı tasarım sistemini kullanır.

İşletme sahibi gerçek çalışma bilgisi bulunmadığını belirtmiş ve gerçekçi senaryolar hazırlanmasını istemiştir. Senaryolar açıkça **Örnek senaryo** etiketi taşır ve yapılmış hizmet kaydı olmadıkları sayfalarda açıklanır. Bunlar müşteri yorumu, vaka kanıtı veya deneyim iddiası olarak kullanılmaz. Fiyat, dakika, ekip mevcudu, sertifika ve şube bilgisi uydurulmaz.

30 ilçe, 189 mahalle/semt/konum ve 29 güzergâh/sanayi sayfasının editoryal kayıtları ayrı JSON girdileridir. Her bölge sayfasında konuma özel açıklamalar, farklı örnek senaryo ve iki ilgili soru bulunur. 8 hizmet sayfasına farklı arıza/taşıma senaryoları ve hizmete özel sorular eklenir. Hizmet dizini, iletişim ve bölge dizini kendi kullanım amaçlarına göre geliştirilir. Ana sayfa, fiyat ve işletme açıklaması farklı amaçlar için mevcut ayrıntılı metinlerini korur.

**Gerçek yer bilgisi ile örnek durum ayrı kaynaklardır.** Valilik, belediye, İBB açık veri, KGM ve resmî tesis kaynakları yer kimliği için kullanılır. Muhtarlık kaydındaki yol, çekici işletmesinin şubesi veya aracın alınış noktası değildir. Veri tablosunda kişisel isim ve telefonlar yayımlanmaz.

EVKA-7’nin Gaziemir ilişkisi içerik ve breadcrumbs içinde düzeltilir; eski URL bağlantı uyumluluğu için korunur. Nazilli’nin Aydın ilçesi olduğu açıkça belirtilir ve İzmir mahallesi olarak sunulmaz; İzmir bağlantılı transfer talebi olarak ayrı grupta yer alır. Belkahve devlet yolu geçidi ile otoyol tüneli birbirine eşitlenmez. Aynı adın birden fazla ilçede veya yolda kullanıldığı yerlerde kesin tek adres iddia edilmez.

Çataltepe, Esenkent ve 7. Sanayi gibi kesin yer kimliği doğrulanamayan adlarda sokak veya tesis uydurmak yerine adresi netleştirmeye yönelik rehber ve varsayımsal durum kullanılır. Senaryo bulunması yer kimliğini doğrulamaz. Bu kayıtlar içerik incelemesinde ayrıca işaretlenir.

## Kontroller

`python3 tools/audit_content.py` her bölge girdisinin üç ayrı açıklama bölümü, örnek senaryo ve soru içerdiğini; uzun paragrafların birebir kopya olmadığını kontrol eder. Yer adları çıkarılmış metinlerin dört kelimelik parçaları arasında benzerlik karşılaştırması yaparak editoryal inceleme çiftlerini raporlar. Sekiz hizmet senaryosunun ayrı ve görünür etiketle işlendiği de denetlenir. Bu kontrol, anlam benzerliğini, doğruluğu veya kapsamlılığı tek başına kanıtlamaz; otomatik rapor bir Google SEO puanı değildir.

`python3 tools/validate.py --public` başlık/açıklama tekilliği, canonical, H1, JSON-LD, dahili bağlantı ve fragment, referans kapsamı, yönlendirme, robots ve sitemap bütünlüğünü denetler. 262 içerik sayfası önceki kullanıcı kararı doğrultusunda indekslemeye uygun kalır; 404 kapsam dışındadır.

İçerik politikası: [Google’ın faydalı içerik rehberi](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) ve [spam politikaları](https://developers.google.com/search/docs/essentials/spam-policies). Belirli bir kelime sayısı veya kurmaca örnek adedi için metin şişirmek yerine sayfanın ihtiyacını açıklamak esas alınır. Sayfaya özel metin, aramada ilk sıra garantisi vermez. Alan adı DNS/SSL ve Google’a açık erişim bu içerik çalışmasından ayrı yayın gereksinimleridir.

## Yer kimliği incelemesinin sınırı

Altı kayıtta kesin tek yer eşleşmesi halen sınırlıdır: Altınevler (kısmi), Betonyol ve Tekeli–Türkmen (birden çok olası tarif), Çataltepe ve Esenkent (çözülememiş), 7. Sanayi Sitesi (tesis adresi doğrulanamamış). Örneklerin eklenmesi bu adresleri doğrulanmış hale getirmez. Nazilli’nin Aydın’da olması ayrı bir kapsam düzeltmesidir. Bu sayfalarda hedef, belirsiz adı kesin mahalleye çevirmek yerine gerçek adresi ve araç durumunu doğru sormaktır.

## Uygulanan kapsam

248 bölge sayfasının ayrı rehberleri ve 8 hizmet sayfasının örnekleri ile toplam 256 farklı senaryo kullanılır. Bölge sayfalarında 496 ilgili soru vardır. Altı ana/dizin/bilgi sayfası kendi amacıyla düzenlenir; her sayfaya gereksiz bir kurmaca hikâye yerleştirilmez. Ortak navigasyon, iletişim, kaynak açıklaması ve prosedür terimleri normal olarak tekrar edebilir. Uzun birebir paragraf kopyası ve yer adları çıkarılmış metinlerin yüksek benzerliği denetlenir. Kontrol sonuçları `unique-content-audit.json` dosyasındadır.
