"""Kaynaklı yer bilgileri; işletme deneyimi veya canlı yol durumu üretmez."""
from pathlib import Path
from html import escape as e
import json
ROOT = Path(__file__).parent
DISTRICT_DATA = json.loads((ROOT/'research-districts.json').read_text())['districts']
NEIGHBORHOODS = {row['path']: row for row in json.loads((ROOT/'official-neighborhoods.json').read_text())['matches']}
ROUTES = json.loads((ROOT/'research-routes.json').read_text())['regions']
CHECKED = '9 Ekim 2026'

def turkish_title(value):
    words=value.replace("İ", "i").replace("I", "ı").lower().split()
    return " ".join(("İ" if word[0]=="i" else word[0].upper())+word[1:] for word in words)

def source_note(sources):
    links = ' · '.join(f'<a href="{e(s["url"],quote=True)}" rel="external">{e(s["title"])}</a>' for s in sources)
    return f'<div class="source-note">Yer bilgisi kaynakları: {links}<br>Kaynak kontrolü: {CHECKED}. Konum notları yolun anlık durumunu veya ekip adresini göstermez.</div>'

def district_sections(key):
    row = DISTRICT_DATA[key]
    facts = '<ul class="local-points">' + ''.join(f'<li>{e(f)}</li>' for f in row['facts']) + '</ul>'
    return [(row['name']+' içinde konumu doğru belirlemek', facts + '<p>'+e(row['paragraph'])+'</p>'+source_note(row['sources']))]

def region_sections(item):
    if item['kind'] == 'ilceler':
        # Katalogda ilçe anahtarları canonical ilçe URL'sinden alınır.
        return district_sections(item['path'].strip('/').split('/')[-1])
    if item['path'] in NEIGHBORHOODS:
        row = NEIGHBORHOODS[item['path']]
        matches = row['matches']
        places = '<ul class="local-points">'+''.join(f'<li>{e(m["district"])} / {e(turkish_title(m["name"]))}</li>' for m in matches)+'</ul>'
        extra = 'Bu ad birden fazla ilçenin kaydında bulunuyor. İlgili ilçeyi seçmeden yalnızca mahalle adıyla yönlendirme yapılmamalıdır.' if len(matches)>1 else f'{e(matches[0]["district"])} ilçe bilgisini konum bağlantınıza ekleyin. Mahallenin merkezini gösteren bir harita noktası, aracın alınacağı adresin yerine geçmez.'
        text = f'<p>İzmir Büyükşehir Belediyesinin muhtarlık kayıtlarında {e(item["name"])} adı aşağıdaki ilçe bilgisiyle eşleşiyor:</p>{places}<p>{extra} Sokak, bina veya işletme girişini paylaşarak alınış yerini netleştirebilirsiniz.</p>'
        return [('Mahalle adı ve ilçe eşleşmesi', text+source_note([{'url':matches[0]['source'],'title':'İBB Açık Veri — Muhtarlıklar'}]))]
    row = ROUTES.get(item['path'])
    if row and row['status'] == 'verified_static_facts':
        facts = '<ul class="local-points">'+''.join(f'<li>{e(f)}</li>' for f in row['facts'])+'</ul>'
        return [('Güzergâh ve konum bilgisi',facts+'<p>'+e(row['guidance'])+'</p>'+source_note(row['sources']))]
    return []
