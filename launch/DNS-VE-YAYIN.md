# izmircekiciyardimi.com — DNS ve yayın

Alan adı projeye eklendi; DNS doğrulaması bekleniyor. Özel önizleme: https://izmir-oto-cekiciniz.cinarservisinfo2.chatgpt.site

## Gerekli DNS kayıtları

Alan adını yönettiğiniz sağlayıcıda aşağıdaki kayıtları ekleyin. Sağlayıcınız tam alan adı yerine göreli ad istiyorsa TXT kayıtlarında yalnızca ilk etiketi kullanın.

| Tür | DNS adı | Değer |
| --- | --- | --- |
| A | @ | 162.159.143.30 |
| A | @ | 172.66.3.26 |
| TXT | _openai-site-verification.izmircekiciyardimi.com | openai-site-verification=9efvN8R1J6AU5JVuSauEep07zwcxSR-mX9rq0a6C3e8 |
| TXT | _cf-custom-hostname.izmircekiciyardimi.com | 7b8f20fc-7e43-41e9-8adf-cd6207cbc369 |

## Google için ilk yayın

DNS kayıtlarının doğrulanması tek başına Google erişimini açmaz; site halen sahibine özel erişimdedir. Kamuya açık yayın için erişim ayarı ve üretim derlemesi birlikte değiştirilmeli.

1. Alan adı ve SSL doğrulamasının tamamlanması.
2. `python3 build.py --public` ile üretim çıktısı: canonical ve diğer mutlak adresler https://izmircekiciyardimi.com olacak. 262 içerik sayfası index,follow; 404 noindex. Sitemap tüm 262 canonical adresi içerir.
3. Yeni sürümü kamuya açık erişimle yayımlama.
4. Search Console alan adı doğrulaması ve https://izmircekiciyardimi.com/sitemap.xml gönderimi.

Hazır ilk aşama sitemap dosyası: `launch/sitemap.xml`. Sites önizlemesinin sitemap’i Google’a gönderilmemeli.

İşletme sahibinin isteğiyle tüm 248 bölge yolu `index-regions.json` kapsamındadır. Gerçek kayıt bulunmayan bölgeler için iş örneği veya müşteri yorumu eklenmez. Sitemap gönderimi tarama ve indeksleme garantisi değildir.

Mevcut izmircekicioto.com sitesinin DNS veya içeriği değiştirilmedi. `url-mapping.json`, referanstaki 275 adresin yeni sitedeki karşılıklarını içerir. Eski sitede 301 geçişi ayrıca uygulanmadı.
