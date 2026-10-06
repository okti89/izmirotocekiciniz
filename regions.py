"""Bölge sayfaları: tek içerik adresi, kaynak kapsamı ve aşamalı indeksleme."""
from pathlib import Path
from html import escape as e
from urllib.parse import quote
import json,re
DISTRICTS='Aliağa Balçova Bayındır Bayraklı Bergama Beydağ Bornova Buca Çeşme Çiğli Dikili Foça Gaziemir Güzelbahçe Karabağlar Karaburun Karşıyaka Kemalpaşa Kınık Kiraz Konak Menderes Menemen Narlıdere Ödemiş Seferihisar Selçuk Tire Torbalı Urla'.split()
def slug(text):return re.sub(r'[^a-z0-9]+','-',text.translate(str.maketrans('ÇĞİÖŞÜçğıöşü','CGIOSUcgiosu')).lower()).strip('-')
# Yalnızca eşdeğer yer/adres yazımları birleştirilir; farklı mahalleler birleştirilmez.
ALIASES={
'/izmir-cekici':'/', '/ayrancilar-cekici':'/torbali-ayrancilar-cekici',
'/isikkoy-cekici':'/isikkent-cekici','/kisikkoy-cekici':'/kisikkoy-sanayi-sitesi-cekici',
'/limanreis-cekici':'/liman-reis-cekici','/yaka-cekici':'/yaka-mahallesi-cekici',
'/yali-cekici':'/yali-mahallesi-cekici','/yaka-koyu-cekici':'/yaka-mahallesi-cekici',
'/cesme-otoyolu-cekici':'/izmir-cesme-otoyolu-cekici','/aydin-otoban-cekici':'/izmir-aydin-otoyolu-cekici',
'/sabuncubeli-cekici':'/sabuncubeli-tuneli-cekici','/belkahve-cekici':'/belkahve-rampasi-cekici',
'/istanbul-yolu-cekici':'/istanbul-otoyolu-cekici','/ankara-otoyolu-cekici':'/ankara-yolu-cekici',
'/bursa-otoyolu-cekici':'/bursa-yolu-cekici'}
PARENTS={
'alacati':'Çeşme','ilica':'Çeşme','boyalik':'Çeşme','altinkum':'Çeşme','dalyan':'Çeşme','ildir':'Çeşme','sifne':'Çeşme','16-eylul':'Çeşme','ovacik':'Çeşme','ciftlikkoy':'Çeşme',
'alsancak':'Konak','goztepe':'Konak','hatay':'Konak','kordon':'Konak','pasaport':'Konak','bostanli':'Karşıyaka','mavisehir':'Karşıyaka','sirinyer':'Buca','pinarbasi':'Bornova','isikkent':'Bornova','sarnic':'Gaziemir','havalimani':'Gaziemir','ucyol':'Karabağlar','kisik':'Menderes','kisikkoy-sanayi-sitesi':'Menderes','buca-golet':'Buca','belenbasi':'Buca','liman-reis':'Güzelbahçe',
'camdibi':'Bornova','ozkanlar':'Bornova','cesmealti':'Urla','altindag':'Bornova','basmane':'Konak','kaynaklar':'Buca','urla-iskele':'Urla','urkmez':'Seferihisar',
'evka1':'Buca','evka2':'Çiğli','evka3':'Bornova','evka4':'Bornova','evka5':'Çiğli','evka6':'Çiğli','evka7':'Çiğli'}
EDITORIAL={
'aliaga':('Aliağa’da tesis girişini ve yol konumunu ayırın.','Liman yolu veya sanayi tesisi yakınındaki bir araç için tesisin adı kadar giriş kapısı da önemlidir. Aliağa merkezindeki talep ile Yeni Şakran hattındaki talepte alınacak adresi ayrı ayrı belirleriz. Yüklü ticari araçta toplam ağırlık ve teslim edilecek işletmenin kabul koşulları görüşülmelidir.'),
'balcova':('Balçova’da cadde ile otopark erişimini birlikte değerlendirelim.','Mithatpaşa ve Ata Caddesi çevresindeki taleplerde araç sokakta mı, bir işletmenin otoparkında mı, yoksa kapalı bir katta mı bulunuyor? Bu ayrım yükleme erişimini belirler. İnciraltı yönünden veya otoyol girişinden alınacak araç için yol yönü ve teslim adresi de paylaşılmalıdır.'),
'bayindir':('Bayındır merkezinden bağlantı yollarına farklı konumlar.','Torbalı–Bayındır yolundaki bir araç ile ilçe merkezindeki servis transferi aynı alınış noktasına sahip değildir. Canlı veya Zeytinova yönüyle konum tarif ederken bir kavşak ya da yol işaretini ekleyin. Ana yoldan ayrılmış bir araçta zeminin ve yükleme alanının fotoğrafı planlamayı kolaylaştırır.'),
'bayrakli':('Bayraklı’da bulunduğunuz yol seviyesi önemli.','Altınyol üzerindeki bir araçla iç sokak veya otoparktaki araç için giriş farklı olabilir. Manas Bulvarı ve çevresinde işletme, bina ve kat bilgisi; ana yol bağlantısında ise gidiş yönü değerlendirilir. Hastane veya adliye çevresinden alınışta araç girişinin hangi kapıda olduğunu paylaşın.'),
'bergama':('Bergama merkezini uzun bağlantı güzergâhlarından ayırın.','Kozak Yaylası yolu, Soma bağlantısı ve İzmir–Çanakkale hattı aynı konum tarifine indirgenemez. İlk görüşmede hangi bağlantıda bulunduğunuzu ve son geçtiğiniz yer işaretini belirtin. Bergama’daki bir servise teslim ile başka ilçeye transfer için ayrı mesafe ve erişim planı yapılır.'),
'beydag':('Beydağ’da baraj, merkez ve bağlantı yolu tarifleri.','Ödemiş–Beydağ yolu ile baraj yönündeki talebin alınış noktası farklıdır. Beydağ veya Nazilli yönünü söylemenin yanında konum bağlantısı ve yolun girişini paylaşın. Aracın ana asfalt üzerinde mi yoksa yan yolda mı olduğu, uygun yükleme erişiminin değerlendirilmesine yardımcı olur.'),
'bornova':('Bornova’da ana yol, kampüs ve sanayi erişimi farklıdır.','Ankara Caddesi veya çevre yolu bağlantısındaki bir araç için yön bilgisi; kampüs çevresinde giriş kapısı; Işıkkent ve Pınarbaşı’nda işletme erişimi öne çıkar. Aracın kapalı bir alanda olması ve tekerleklerinin hareket etmemesi yükleme seçimini değiştirebilir. Teslim alınacak servis önceden belirlenmelidir.'),
'buca':('Buca’da sokak, kampüs ve otoyol bağlantısını belirtin.','Şirinyer’de cadde üzerindeki talep, Tınaztepe çevresindeki bir otopark talebi ve Kaynaklar bağlantısındaki araç için aynı erişim planı kullanılamaz. Bulunduğunuz mahallenin yanında aracın girişe göre yerini bildirin. Teslim noktası Gaziemir veya başka bir ilçedeyse bu adresi görüşmenin başında paylaşın.'),
'cesme':('Çeşme’de sahil hattı ile otoyoldaki konumu ayırın.','Alaçatı, Ilıca, Dalyan ve Çiftlikköy yönleri bir talebin genel yerini anlatabilir; ancak çekicinin araçla buluşacağı nokta için tam konum gerekir. Aracın otel girişinde, açık otoparkta veya otoyolda bulunması farklı erişim koşulları doğurur. Servis transferinde hedef ilçeyi ve adresi birlikte belirleriz.'),
'cigli':('Çiğli’de sanayi tesisi girişine dikkat.','Anadolu Caddesi üzerindeki binek araç talebi ile İAOSB veya Ata Sanayi içindeki ticari araç transferi farklı koşullara sahiptir. Tesis adı, kapı numarası, yük durumu ve giriş saatini paylaşın. Sasalı bağlantısında yolun yönünü ve ana yoldan ayrılıp ayrılmadığınızı da belirtin.'),
'dikili':('Dikili’de sahil ve ana yol konumunu netleştirin.','Çandarlı, Bademli veya Salihleraltı yönünden talepte bulunduğunuzda yalnızca sahil hattının adını vermek yeterli olmaz. Yakın bir kavşak, otopark girişi ve konum bağlantısı araç alınışını planlamaya yardımcı olur. E87 üzerindeyseniz gidiş yönünü ve yakın çıkışı ekleyin.'),
'foca':('Foça ve Yeni Foça için ayrı alınış bilgisi.','İzmir–Foça yolu, Yeni Foça sahili ve Bağarası bağlantısı farklı güzergâhlardır. İlk görüşmede hangi hat üzerinde olduğunuzu belirterek gerçek konumunuzu paylaşın. Köy yolunda kalan aracın bulunduğu zemini ve çevresindeki yükleme alanını gösteren fotoğraf ekipman değerlendirmesini kolaylaştırır.'),
'guzelbahce':('Güzelbahçe’de otoyol çıkışı ve ilçe içi adresler.','Mithatpaşa Caddesi’ndeki bir aracı almak ile Çeşme otoyolu çıkışındaki talebi karşılamak için farklı girişler gerekebilir. Seferihisar yönündeyseniz yolun hangi bölümünde bulunduğunuzu belirtin. İşletme veya konut girişindeki talepte otopark yüksekliği ve rampa bilgisi de değerlendirilir.'),
'karabaglar':('Karabağlar’da sanayi ve konut erişimi.','Yeşillik Caddesi, Uzundere bağlantısı ve sanayi sitesi içindeki talepler için tam konumla birlikte araç çevresinin fotoğrafını paylaşın. İşletmeye teslim edilecek araçta kabul kapısı, sokakta alınacak araçta park düzeni önemlidir. Hasar veya kilitli tekerlek varsa standart transferden farklı bir yükleme ihtiyacı doğabilir.'),
'karaburun':('Karaburun’da yarımada üzerindeki gerçek noktayı belirleyin.','Mordoğan, İskele veya Küçükbahçe yönünü bildirmek yararlıdır; fakat yarımada yolunda araç alınışını planlamak için konum bağlantısı gerekir. Aracın ana yolun dışında ya da eğimli bir noktada bulunması durumunda fotoğraf ekleyin. Teslimin Karaburun’da mı yoksa başka ilçede mi yapılacağını görüşmede netleştirin.'),
'karsiyaka':('Karşıyaka’da sahil hattı ve iç bağlantılar.','Bostanlı İskele çevresinde kalan araçla Girne Bulvarı veya Örnekköy yönündeki araç aynı girişten alınmayabilir. Sahil caddesinde yön, apartman otoparkında kat ve giriş yüksekliği bilgisi önem taşır. Akü veya marş sorunu için yerinde desteğin uygunluğu da araç modeliyle birlikte değerlendirilir.'),
'kemalpasa':('Kemalpaşa’da tesis ve otoyol konumları.','KOSBİ içindeki bir transferde işletme kapısı, araç üstyapısı ve yük bilgisi gerekir. Otoyol veya Ankara Asfaltı bağlantısında ise yolun adı ve gidiş yönü öne çıkar. Yüklü ticari aracın ölçüleri ve teslim edilecek tesisin erişimi, ekipman planlamasında ayrıca görüşülür.'),
'kinik':('Kınık’ta merkez, Poyracık ve bağlantı hattını ayırın.','Bergama–Soma yolu üzerindeki talep ile Poyracık veya Yayakent yönündeki talep farklı konumlar olabilir. Yol işareti ve gerçek konum bağlantısını birlikte paylaşın. OSB girişinden alınacak ticari araçta yük durumu ve işletme kapısı belirlenmeden standart taşıma planı verilmez.'),
'kiraz':('Kiraz’da bağlantı yönü ve servis tercihi.','Ödemiş–Kiraz veya Alaşehir yönünden talepte yolun yönünü ve bulunduğunuz noktayı bildirin. İlçe sanayisine teslim için servis adresi ile kabul saatini görüşmede paylaşın. Ana yoldan uzak bir konumda aracın yüklemeye erişimi, konum ve fotoğraf üzerinden ayrıca değerlendirilir.'),
'konak':('Konak’ta doğru sokak ve giriş, ilçe adı kadar önemli.','Basmane, Çankaya, Alsancak ve sahil hattındaki talepler birbirinden farklı erişim koşullarına sahiptir. Kapalı otopark veya vale alanında kat ve giriş; ana cadde üzerinde yol yönü belirtilmelidir. Çekici yüklemesi için aracın mevcut hasar durumu ve çevresindeki alan birlikte değerlendirilir.'),
'menemen':('Menemen’de ana yol ve sanayi transferleri.','Çanakkale Asfaltı, çevre yolu, Ulukent bağlantısı ve sanayi içindeki bir talepte araç konumu farklı tarif edilmelidir. Tesis girişinden alınacak araç için işletme adı ve kapı; ana yol üzerindeki araç için gidiş yönü ve yakın çıkış paylaşın. Teslim ilçesi değişirse transfer mesafesini ayrıca belirleriz.'),
'narlidere':('Narlıdere’de gişe ile sokak adresini karıştırmayın.','Otoyol gişelerindeki bir araç için yol yönü ve giriş bilgisi, Sahilevleri veya Mithatpaşa Caddesi çevresinde ise tam sokak adresi gerekir. Konut otoparkındaki aracın giriş yüksekliğini ve bulunduğu katı belirtin. Aracın hareket etmemesi erişim değerlendirmesine ek ekipman ihtiyacı katabilir.'),
'odemis':('Ödemiş’te merkez, yayla ve bağlantı yolları.','Birgi, Gölcük–Bozdağ ve Tire bağlantıları farklı taşıma mesafeleri doğurabilir. Talebinizde hangi güzergâhta bulunduğunuzu ve teslim noktasını birlikte belirtin. Yayla veya yan yolda kalan aracın bulunduğu zemin ve yükleme alanı fotoğrafları erişim planını destekler.'),
'seferihisar':('Seferihisar’da Sığacık ve sahil yolunu ayrı tarif edin.','İlçe merkezi, Sığacık yolu ve Kuşadası yönündeki sahil hattı aynı alınış noktası değildir. Konum bağlantısına yakın bir işletme, otopark veya yol işaretini ekleyin. Araç güvenle hareket edemiyorsa yürür aksam ve hasar bilgisiyle uygun transfer seçeneği değerlendirilir.'),
'selcuk':('Selçuk’ta gişe, turistik alan ve servis girişleri.','Efes, Pamucak ve Şirince yönünden talepte otopark ya da yol girişinin hangi noktada olduğunu belirtin. Selçuk gişeleri veya Kuşadası bağlantısındaysanız gidiş yönünü ekleyin. Başka bir ilçedeki servise teslim için alınış ve bırakılış adreslerini aynı görüşmede netleştirmek gerekir.'),
'tire':('Tire’de OSB ve ilçe sanayisi için kapı bilgisi.','TOSBİ içindeki ticari araç ile merkezdeki binek araç farklı ekipman ve erişim ihtiyacına sahip olabilir. İşletme girişini, yük durumunu ve kabul saatini paylaşın. Selçuk ya da Ödemiş bağlantısındaki bir araçta yol yönü ve yakın kavşak, alınış noktasını belirlemeyi kolaylaştırır.'),
'torbali':('Torbalı’da mahalle ile ana bağlantıyı birlikte belirtin.','Ayrancılar, Pancar ve ilçe merkezindeki araçlar için tek bir konum tarifi kullanılamaz. İzmir–Aydın hattında yön ve yakın çıkış; sanayi içindeki talepte işletme kapısı ve yük bilgisi paylaşılmalıdır. Teslim adresi farklı bir ilçedeyse mesafe ve taşıma kapsamı buna göre belirlenir.'),
'urla':('Urla’da otoyol, İskele ve kırsal bağlantı talepleri.','Urla çıkışındaki bir araç ile İskele, İçmeler veya Kuşçular yönündeki bir araç farklı erişim koşullarına sahiptir. Yolun adını ve gerçek konumu paylaşın; tesis veya otopark içindeyseniz giriş noktasını ekleyin. Ana yoldan ayrılan konumlarda yükleme alanını gösteren fotoğraf yararlı olur.')}
# Sayfa başına gerçek konum farkını anlatan editoryal notlar.
LOCAL_NOTES={
'alsancak':('Kordon, liman ve otopark talepleri','Alsancak’taki talepte sahil caddesi ile iç sokak veya otopark girişini ayrı belirtin. Vale noktasındaki bir araçta anahtarın kimde olduğu ve aracın hangi katta bulunduğu yükleme planını etkiler. Kordon, liman veya Kıbrıs Şehitleri çevresi genel bir tarif olabilir; aracın yanındaki gerçek konum bağlantısını ekleyin.'),
'bostanli':('İskele, pazaryeri ve sahil hattı','Bostanlı İskele veya pazaryeri çevresinde bulunduğunuzu söylerken aracın cadde üzerindeki yönünü ve girişini ekleyin. Sahil hattındaki araçla apartman otoparkındaki araç için farklı yaklaşım gerekebilir. Tekerlek veya direksiyon kilidi varsa konumla birlikte belirtin.'),
'mavisehir':('AVM ve site otoparkına erişim','Mavişehir’de bir AVM veya site otoparkındaki aracın alınması için kapı, kat ve yükseklik bilgisi gerekir. MaviBahçe ya da Ege Park adını vermenin yanında aracın bulunduğu giriş noktasını paylaşın. Otopark rampası ve aracın hareket durumu uygun yüklemeyi belirler.'),
'sarnic':('Sanayi ile havalimanı bağlantısı','Sarnıç’ta işletme önünden alınacak ticari araçta kapı ve yük bilgisi; havalimanı çevre yolu bağlantısında yol yönü önemlidir. Çamlık Caddesi veya Menderes yönü yalnızca genel bir tarifse tam konum ekleyin. Gaziemir çıkışlı ekibin mevcut durumu görüşmede değerlendirilir.'),
'isikkent':('İşletme ve site girişini belirtin','Işıkkent’te araç bir işyerinin bahçesinde veya sanayi içindeyse işletme kapısını ve yükleme alanını paylaşın. Yüklü hafif ticari araç ile binek aracın ağırlık ve erişim ihtiyacı aynı olmayabilir. Teslim noktası Pınarbaşı veya başka servis alanındaysa hedef işletmenin kabul koşulları ayrıca belirlenir.'),
'pinarbasi':('Sanayi içi transferde teslim kapısı','Pınarbaşı’nda sanayi veya servis transferi için alınacak işletmeyle teslim edilecek işletmeyi ayrı ayrı belirtin. Özellikle çalışmayan aracın tekerlekleri kilitliyse veya alçak bir rampada bulunuyorsa fotoğraf paylaşın. Kemalpaşa Caddesi ve sanayi girişleri genel tarif olarak kullanılabilir; tam konumun yerini tutmaz.'),
'sirinyer':('Cadde ve istasyon çevresinde alınış','Şirinyer’de Menderes Caddesi, Forbes çevresi veya İZBAN yakınındaki talebinizde aracın hangi tarafta bulunduğunu belirtin. Sokak içinde yükleme alanı ile kapalı otoparkta kat bilgisi farklı gereksinimlerdir. Servisin adresini görüşmede paylaşarak transferin son noktasını netleştirin.'),
'goztepe':('Sahil ile üst cadde bağlantısı','Göztepe’de sahil bulvarı üzerindeki konum ile Mithatpaşa veya İnönü Caddesi bağlantısındaki konum aynı yaklaşımla tarif edilmez. İskele veya stadyum çevresini belirtirken cadde tarafını ve aracın tam yerini ekleyin. Otoparktan alınacak araçta giriş yüksekliği ayrıca sorulur.'),
'hatay':('İnönü Caddesi ve bağlantı sokakları','Hatay tarifinde Nokta Kavşağı, metro veya Poligon bağlantısını belirtmek yardımcı olabilir. Aracın ana cadde üzerinde mi, ara sokakta mı yoksa bina otoparkında mı olduğunu da paylaşın. Rampa veya dar giriş varsa yükleme yöntemi konum ve araç fotoğrafıyla değerlendirilir.'),
'ucyol':('Kavşak ve otopark konumunu ayırın','Üçyol’da metro veya kavşak çevresi genel bir konum tarifidir. İnönü, Eskiizmir ve bağlantı sokaklarında bulunduğunuz yönü ve bina girişini belirtin. Tekerlekleri kilitli bir araç, girişteki alanı kullanamadığı için ek yükleme değerlendirmesi gerektirebilir.'),
'alacati':('Gişe, Hacımemiş ve liman yönü','Alaçatı gişeleri, Hacımemiş bölgesi ve Port Alaçatı yolu farklı alınış noktalarıdır. Araç otel veya işletme girişindeyse girişin fotoğrafı; otoyoldaysa yol yönü ve yakın çıkış bilgisi gerekir. Motosiklet taleplerinde aracın modeli ve sabitlemeyi etkileyen hasarı da paylaşın.'),
'evka1':('EVKA 1 adını tam adresle tamamlayın','EVKA 1 adını kullanırken Buca’daki mahalle ve sokak bilgisini de iletin. Murathan veya farklı bir mahalledeki aracın tam konumu, genel semt adından daha belirleyicidir. Site veya bina otoparkında blok, kat ve giriş yüksekliği bilgisi yükleme erişimini netleştirir.'),
'havalimani':('Terminal ve otopark katı','Havalimanında kalan araç için terminal, otopark katı ve giriş bilgisini birlikte iletin. Aracın anahtarı, kapı erişimi ve hareket durumu görüşmede netleştirilir. Kapalı otopark yüksekliği sebebiyle standart çekicinin erişimi uygun olmayabilir; yöntem konuma göre değerlendirilir.')}
ROAD_NOTES={
'izmir-cevre-yolu':('Çevre yolunda bağlantı ve yön bilgisi','İzmir Çevre Yolu talebinde O-30, yön, yakın kavşak veya çıkış bilgisini birlikte paylaşın. Bayraklı, Bornova, Buca veya Gaziemir bağlantısı tek başına aracın tam noktasını göstermeyebilir. Konum bağlantısına yolun üzerinde görünen işareti eklemek yanlış girişten yaklaşılmasını önlemeye yardımcı olur.'),
'izmir-aydin-otoyolu':('Aydın yönü ile İzmir yönünü ayırın','İzmir–Aydın otoyolunda O-31 yol bilgisi, gidiş yönü ve yakın gişe veya çıkış gerekir. Torbalı, Belevi ya da Selçuk adıyla birlikte aracın otoyolda mı bağlantı yolunda mı olduğunu belirtin. Aracın bırakılacağı servis adresini paylaşarak transferin toplam güzergâhını belirleyelim.'),
'izmir-cesme-otoyolu':('Gişe ve bağlantı çıkışını belirtin','İzmir–Çeşme otoyolunda O-32, gidiş yönü ve yakın çıkışı paylaşın. Urla, Güzelbahçe ve Alaçatı bağlantılarında aracın gişeden önce mi sonra mı olduğunu açıklayın. Çeşme ilçesindeki bir sokak adresiyle otoyoldaki alınış noktası aynı şekilde tarif edilmemelidir.'),
'sabuncubeli-tuneli':('Tünel ile yaklaşım yolunu ayırın','Sabuncubeli talebinde aracın tünel içinde mi, çıkışta mı yoksa yaklaşım yolunda mı bulunduğunu belirtin. İzmir veya Manisa yönü ve konum bağlantısı beraber değerlendirilir. Ekipmanın araca erişimi, aracın hareket durumu ve ilgili yol koşulları üzerinden planlanır.'),
'belkahve-rampasi':('Rampa hattında yolun türünü belirtin','Belkahve Rampası tarifini yolun tabeladaki adı ve gidiş yönüyle tamamlayın. Otoyol, devlet yolu ve bağlantı yolu farklı girişlere sahip olabilir. Rampada kaldığınızı söylemenin yanında yakın çıkış veya görünür işareti ekleyin; kurtarma gereksinimi varsa araç ve zemin fotoğrafını paylaşın.'),
'belkahve-tunelleri':('Tünel giriş ve çıkışını netleştirin','Belkahve tünelleri için hangi giriş veya çıkışa yakın olduğunuzu ve yolun yönünü bildirin. Aracın tünelde mi yoksa bağlantı güzergâhında mı bulunduğunu ayırmak ekip erişimi açısından önemlidir. Aracın yüksekliği, hasarı ve hareket edebilirliği ekipman planına eklenir.'),
'bayrakli-tunelleri':('Bayraklı tünellerinde yön ve bağlantı','Bayraklı tünellerindeki talep için tünel adı, gidiş yönü ve aracın tünel içi veya çıkışındaki konumu gerekir. İzmir Çevre Yolu bağlantısının hangi bölümünde bulunduğunuzu paylaşın. Hasarlı veya hareket edemeyen araçta doğrudan transfer ile kurtarma ihtiyacı ayrı değerlendirilir.'),
'konak-tuneli':('Konak Tüneli ile bağlantı yolları','Konak Tüneli talebinde giriş ve çıkış yönünü, aracın tünel içinde mi bağlantı yolunda mı bulunduğunu paylaşın. Yalnızca Konak ilçesini belirtmek uygun yaklaşımı belirlemek için yeterli değildir. Konum bağlantısı ve yol üzerindeki görünür işaretle alınış noktasını netleştirelim.'),
'altinyol-sahil-yolu':('Altınyol ile sahil adresini ayırın','Altınyol üzerinde aracın yolun hangi yönünde bulunduğunu ve yakın bağlantıyı belirtin. Sahil çevresindeki bir otopark talebiyle ana yol üzerindeki alınış farklı girişler gerektirebilir. Aracın konum fotoğrafında çevredeki yol işaretinin görünmesi yaklaşımın belirlenmesine yardımcı olur.'),
'istanbul-otoyolu':('Uzun hat üzerinde gerçek kesimi belirtin','İstanbul–İzmir otoyolu genel bir güzergâh adıdır; aracın bulunduğu kesimi, gidiş yönünü ve yakın çıkışı belirtin. İzmir çevresinden uzak taleplerde hizmet uygunluğu ve gerekli ekipman ayrıca görüşülür. Bütün otoyol boyunca sabit ekip veya varış süresi bulunduğu iddia edilmez.'),
'bursa-yolu':('Bursa hattında yol adı ve kesim bilgisi','Bursa yolu veya otoyolu ifadesi araç konumunu tek başına belirlemez. Tabeladaki yol adını, gidiş yönünü ve bulunduğunuz il veya yakın çıkışı paylaşın. İzmir dışındaki talepte mesafe ve ekip uygunluğu netleşmeden yönlendirme ya da süre taahhüdü verilmez.'),
'ankara-yolu':('Ankara yönü, yol türü ve yakın bağlantı','Ankara yolu talebinde bulunduğunuz yolun otoyol mu devlet yolu mu bağlantı yolu mu olduğunu belirtin. Tabeladaki yol adı veya numarası, yön ve yakın kavşak birlikte kullanılmalıdır. İzmir çevresindeki talep ile daha uzaktaki bir noktada taşıma farklı mesafe ve ekipman planı gerektirir.')}
def clean_name(text):
 text=re.sub(r'\s*Çekici(?:\s.*)?$','',text).strip()
 text=re.sub(r'^Evka[- ]?([1-7])$',r'Evka \1',text,flags=re.I)
 if re.match(r'^[1-7]\. Sanayi$',text):text+=' Sitesi'
 return text

def context(record):
 old=record['reference_path'];stem=old.strip('/').removesuffix('-cekici')
 name=clean_name(record.get('heading','')) or record.get('fallback_name',stem)
 if name in DISTRICTS:return name,[name]
 if old.startswith('/torbali-'):return 'Torbalı',['Torbalı']
 if stem in PARENTS:return PARENTS[stem],[PARENTS[stem]]
 paragraphs=' '.join(record.get('hero_paragraphs',[]))
 match=re.search(r'belediye kayıtlarında ([^.,]+?) ilçe bilgisi',paragraphs)
 if match and match[1] in DISTRICTS:return match[1],[match[1]]
 match=re.search(r'mahalle kayıtlarında (.+?) için geçiyor',paragraphs)
 if match:
  candidates=[d for d in DISTRICTS if re.search(r'\b'+re.escape(d)+r'\b',match[1])]
  return (candidates[0] if len(candidates)==1 else None),candidates
 return None,[]

def build_region_catalog(root):
 facts=json.loads((root/'reference-facts.json').read_text());inventory=json.loads((root/'content-backlog.json').read_text())['regions']
 records={x['reference_path']:x for x in facts};groups={}
 def primary(old):
  seen=set()
  while old in ALIASES:
   assert old not in seen,'Alias cycle';seen.add(old);old=ALIASES[old]
  return old
 for item in inventory:
  old=item['reference_path'];key=primary(old)
  if key=='/':continue
  if key not in groups:groups[key]={'references':[],'facts':[]}
  groups[key]['references'].append(old)
  rec=dict(records.get(old,{}));rec['fallback_name']=clean_name(re.sub(r'([a-zçğıöşü])([A-ZÇĞİÖŞÜ])',r'\1 \2',item['reference_label']));groups[key]['facts'].append(rec)
 catalog=[];mapping={'/izmir-cekici':'/'}
 for old,group in groups.items():
  valid=[x for x in group['facts']if x.get('http_status')==200]
  assert valid,('No valid source',old)
  # Birleşen adreslerden en fazla gerçek yer bilgisi olan kaynak seçilir.
  record=max(valid,key=lambda x:(len(x.get('roads',[])),x['reference_path']==old));record=dict(record);record['reference_path']=old
  name=clean_name(record.get('heading','')) or record['fallback_name'];stem=old.strip('/').removesuffix('-cekici')
  if old=='/kisikkoy-sanayi-sitesi-cekici':name='Kısıkköy Sanayi Sitesi'
  if old=='/torbali-ayrancilar-cekici':name='Torbalı Ayrancılar'
  district,candidates=context(record)
  kind='ilceler' if name in DISTRICTS else 'sanayi' if 'sanayi' in old else 'guzergahlar' if any(x in old for x in ['yolu','otoyol','otoban','tunel','belkahve','sabuncubeli'])else 'noktalar'
  if kind=='ilceler':path='/bolgeler/'+slug(name)+'/'
  elif kind=='sanayi':path='/sanayi/'+slug(name)+'/'
  elif kind=='guzergahlar':path='/guzergahlar/'+stem+'/'
  elif district:path='/bolgeler/'+slug(district)+'/'+slug(name.removeprefix(district+' '))+'/'
  else:path='/bolgeler/noktalar/'+slug(name)+'/'
  roads=list(dict.fromkeys(y for x in valid for y in x.get('roads',[])))
  catalog.append({'name':name,'path':path,'kind':kind,'district':district,'candidates':candidates,'roads':roads,'source_note':record.get('hero_paragraphs',[''])[-1],'source_paths':group['references'],'stem':stem})
  for source in group['references']:mapping[source]=path
 assert len({x['path']for x in catalog})==len(catalog),'Canonical path collision'
 return catalog,mapping

def render_regions(root,layout,subhero,buttons,ORIGIN,PUBLIC):
 catalog,mapping=build_region_catalog(root);approved=set(json.loads((root/'index-regions.json').read_text())['indexable_paths']);assert approved <= {x['path'] for x in catalog};by_path={x['path']:x for x in catalog};by_name={x['name']:x for x in catalog}
 for item in catalog:
  name=item['name'];path=item['path'];district=item['district'];kind=item['kind'];stem=item['stem']
  if name in ('Gaziemir','Menderes'):continue
  parent_path='/bolgeler/'+slug(district)+'/'if district and district!=name else '/hizmet-bolgeleri/'
  parent_name=district+' çekici'if district and district!=name else 'Hizmet bölgeleri'
  desc=f'{name} için 7/24 çekici ve yol yardım talebi. '+(f'{district} bağlantılı konum ve erişim bilgileri. 'if district and district!=name else '')+'0536 676 28 66 üzerinden araç bilgisi ve konumunuzu paylaşın.'
  sections=[]
  if kind=='ilceler':
   heading,text=EDITORIAL[slug(name)];sections.append((heading,text))
  elif stem in LOCAL_NOTES:sections.append(LOCAL_NOTES[stem])
  elif stem in ROAD_NOTES:sections.append(ROAD_NOTES[stem])
  elif kind=='guzergahlar':
   if 'tunel' in stem:
    sections.append((name+' için giriş ve çıkış bilgisi',f'{name} talebinde aracın tünel içinde, yaklaşım yolunda veya çıkışında bulunduğunu belirtin. Gidiş yönünü ve yol üzerindeki görünür işareti konum bağlantısıyla birlikte iletin. Aracın hareket durumu, yüksekliği ve hasarı araca uygun ekipmanla erişimin değerlendirilmesinde kullanılır.'))
   else:sections.append((name+' üzerinde alınış noktasını belirleyelim',f'{name} adıyla talep iletirken tabeladaki yol adını veya numarasını, gidiş yönünü ve yakın çıkışı paylaşın. Aracın ana yol üzerinde mi yoksa bir bağlantı veya tesis girişinde mi bulunduğunu belirtin. Böylece yalnızca genel güzergâh adıyla hareket etmek yerine gerçek alınış noktası üzerinden plan yapılabilir.'))
  elif kind=='sanayi':
   sections.append((name+' için işletme ve kapı bilgisi',f'{name} içinde bir araç alınacaksa site numarası veya adıyla birlikte ilçe, sokak ya da blok ve işletme kapısını belirtin. Servise götürülecek aracın kabul edileceği işletme ile çıkacağı işletme farklıysa iki adresi ayrı paylaşın. Giriş yüksekliği, yük durumu ve aracın hareket edebilirliği ekipman değerlendirmesine eklenir.'))
   sections.append(('Alınış ve teslim için kısa kontrol listesi','Serviste bulunan aracın anahtarını teslim edecek kişiyi, işyerinin kabul saatini ve yükleme alanını netleştirin. Araç sökülmüş, tekerlekleri kilitli veya üstyapısı standarttan farklıysa fotoğraf paylaşın. Bu bilgiler olmadan her araç için aynı transfer yöntemi veya sabit fiyat verilmez.'))
  elif len(item['candidates'])>1:
   names=', '.join(item['candidates'])
   sections.append((name+' adını ilçeyle birlikte paylaşın',f'{name} adı, referans yer bilgilerinde {names} ilçeleriyle birlikte geçiyor. Bu adla çekici isterken ilçe, sokak ve tam konum bağlantısını birlikte belirtin. Bir mahalle adının tekrar etmesi, ekibin aynı noktaya yönlendirilmesi gerektiği anlamına gelmez; alınış adresi talep sırasında kesinleştirilir.'))
   sections.append(('Doğru bölgeyi seçmek için',f'İlçeniz aşağıdaki bağlantılarda varsa ilgili bölge rehberini inceleyebilirsiniz. Aracın {name} adıyla bilinen bir site veya tesis içinde bulunması durumunda resmî adresin yanında giriş ve blok bilgisini ekleyin. Konum paylaşırken yalnızca genel semt adını kullanmayın.'))
  elif district:
   sections.append((name+' talebinde '+district+' adresini tamamlayın',f'{name} için alınış adresini {district} ilçe bilgisi, cadde veya sokak ve aracın bulunduğu girişle birlikte paylaşın. Konum bağlantısı, yalnızca mahalle adıyla yapılan tarife göre araca erişimi daha açık hale getirir. Araç bir site ya da otoparktaysa bina, blok veya kat bilgisini de ekleyin.'))
  else:
   sections.append((name+' adını tam konumla eşleştirelim',f'{name} adıyla talep iletirken ilçe ve açık konum bağlantısını paylaşın. Semt, site, tesis ve resmî mahalle adı aynı olmayabilir. Bulunduğunuz noktanın ana yol, sokak veya otopark içinde olması, uygun yükleme erişiminin seçilmesinde belirleyicidir.'))
  if item['roads']:
   sections.append(('Konum tarifinde kullanabileceğiniz noktalar','Aşağıdaki adlar talep ettiğiniz konumu açıklamak için yardımcı olabilir. Bunlar şube, sabit ekip adresi veya garanti edilmiş varış noktası değildir. Aracın gerçek konumunu ayrıca paylaşın.<ul class="local-points">'+''.join('<li>'+e(x)+'</li>'for x in item['roads'])+'</ul>'))
  if district and district!=name and slug(district) in EDITORIAL:
   dh,dt=EDITORIAL[slug(district)]
   sections.append((district+' içindeki bağlantıları birlikte değerlendirelim',dt))
  # Sayfada uzun ortak tanıtım metinleri yerine bölgeye göre önceden doldurulan gerçek talep bağlantısı kullanılır.
  request='Merhaba, '+name+' için çekici/yol yardım talebim var.\nİlçe ve tam konum: \nAraç marka-modeli: \nSorun ve hareket durumu: \nTeslim adresi: '
  wa='https://wa.me/905366762866?text='+quote(request)
  sections.append(('Talebinizi '+name+' bilgisiyle hazırlayın',f'WhatsApp bağlantısı bu bölgenin adını hazır olarak ekler. İlçe ve gerçek konumunuzu, araç modelini, mevcut sorunu ve teslim adresini tamamlayarak gönderebilirsiniz. Yol veya otopark erişimini etkileyen durum varsa aracın çevresini gösteren bir fotoğraf ekleyin.<p><a class="btn" href="{wa}">{e(name)} için WhatsApp ile yazın</a></p>'))
  local_body=''.join(f'<section><h2>{e(h)}</h2><div class="region-copy">{t}</div></section>'for h,t in sections)
  related=[]
  if district and district!=name:related.append((district+' çekici',parent_path))
  if kind=='ilceler':related+=[(x['name']+' çekici',x['path'])for x in catalog if x['district']==name and x['kind']=='noktalar'][:24]
  elif item['candidates']:related+=[(d+' çekici','/bolgeler/'+slug(d)+'/')for d in item['candidates']if d!=district]
  if related:local_body+='<section><h2>İlgili bölge sayfaları</h2><ul class="related-links">'+''.join(f'<li><a href="{p}">{e(n)}</a></li>'for n,p in related)+'</ul></section>'
  local_body+='<section><h2>Aracınız için hizmet seçimi</h2><p>Marş sorunu için yerinde yardım ile hareket edemeyen araç için taşıma farklı değerlendirilir. Araç ve belirti bilgisiyle uygun hizmeti görüşebilirsiniz.</p><ul class="related-links"><li><a href="/hizmetler/oto-cekici/">Oto çekici ve servis transferi</a></li><li><a href="/hizmetler/aku-takviye/">Akü takviye</a></li><li><a href="/hizmetler/motosiklet-cekici/">Motosiklet taşıma</a></li><li><a href="/hizmetler/oto-kurtarma/">Kurtarma ihtiyacı</a></li></ul></section>'
  aside=f'<aside class="aside"><span class="eyebrow">7/24 TALEP HATTI</span><h3>{e(name)} için bize ulaşın.</h3><p>Ücret ve tahmini varış, gerçek konumunuz ve araç durumuyla görüşmede belirlenir.</p><a class="btn" href="tel:+905366762866">0536 676 28 66</a><a class="btn secondary" href="{wa}">WhatsApp ile yazın</a><p style="margin-top:20px">Ana çıkış bölgeleri: Gaziemir ve Menderes. Diğer taleplerde ekip ve mesafe uygunluğu değerlendirilir.</p><a class="text-link" href="/fiyatlandirma/">Ücretlendirme bilgisi</a></aside>'
  body=subhero(name+' çekici ve yol yardım',desc,path,(parent_name,parent_path))+'<section class="section"><div class="wrap detail-grid"><article class="article">'+local_body+'</article>'+aside+'</div></section>'
  layout(path,name+' Çekici ve Yol Yardım | İzmir Oto Çekiciniz',desc,body,ready=path in approved,crumbs=[('Ana sayfa','/'),(parent_name,parent_path),(name+' çekici',path)],service=name+' çekici',area=name)
 (root/'region-catalog.json').write_text(json.dumps({'regions':catalog,'reference_url_mapping':mapping},ensure_ascii=False,indent=2))
 return catalog,mapping
