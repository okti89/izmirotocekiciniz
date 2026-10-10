"""Kaynaklı yer bilgileri; işletme deneyimi veya canlı yol durumu üretmez."""
from pathlib import Path
from html import escape as e
import json
from editorial_content import all_briefs
ROOT = Path(__file__).parent
DISTRICT_DATA = json.loads((ROOT/'research-districts.json').read_text())['districts']
NEIGHBORHOODS = {row['path']: row for row in json.loads((ROOT/'official-neighborhoods.json').read_text())['matches']}
ROUTES = json.loads((ROOT/'research-routes.json').read_text())['regions']
CHECKED = '9 Ekim 2026'
DETAILS=json.loads((ROOT/'official-neighborhood-details.json').read_text())

def turkish_title(value):
    words=value.replace("İ", "i").replace("I", "ı").lower().split()
    return " ".join(("İ" if word[0]=="i" else word[0].upper())+word[1:] for word in words)

def source_note(sources,checked=CHECKED):
    links = ' · '.join(f'<a href="{e(s["url"],quote=True)}" rel="external">{e(s["title"])}</a>' for s in sources)
    return f'<div class="source-note">Yer bilgisi kaynakları: {links}<br>İçerik incelemesi: {checked}. Konum notları yolun anlık durumunu veya ekip adresini göstermez.</div>'

def district_sections(key):
    row = DISTRICT_DATA[key]
    facts = '<ul class="local-points">' + ''.join(f'<li>{e(f)}</li>' for f in row['facts']) + '</ul>'
    return [(row['name']+' içinde konumu doğru belirlemek', facts + '<p>'+e(row['paragraph'])+'</p>'+source_note(row['sources']))]

def region_sections(item):
    row=all_briefs().get(item['path'],{})
    if item['path'] in DETAILS:
        record=DETAILS[item['path']]
        rows=''.join('<tr><td>'+e(m['district'])+'</td><td>'+e(turkish_title(m['name']))+'</td><td>'+e(turkish_title(m['road']))+'</td></tr>' for m in record['records'])
        table='<table class="place-table"><caption>İBB muhtarlık kayıtlarındaki adres referansları. Bu noktalar çekici şubesi veya aracın alınış adresi değildir.</caption><thead><tr><th scope="col">İlçe</th><th scope="col">Mahalle</th><th scope="col">Kaynak kaydındaki yol</th></tr></thead><tbody>'+rows+'</tbody></table>'
        sources=[{'url':record['source'],'title':'İBB Açık Veri — Muhtarlıklar'}]
        seen={record['source']}
        for source in row.get('sources',[]):
            if source['url'] not in seen:sources.append(source);seen.add(source['url'])
        return [('Mahalle adını adres kaydıyla ayırt edin',table+source_note(sources,'11 Ekim 2026'))]
    if row:
        facts=row.get('facts',[])
        sources=row.get('sources',[])
        html=('<ul class="local-points">'+''.join('<li>'+e(text)+'</li>' for text in facts)+'</ul>') if facts else ''
        if sources:html+=source_note(sources,'11 Ekim 2026')
        return [('Yer ve güzergâh bilgisi',html)] if html else []
    if item['kind']=='ilceler':return district_sections(item['path'].strip('/').split('/')[-1])
    row=ROUTES.get(item['path'])
    if row and row['status']=='verified_static_facts':
        facts='<ul class="local-points">'+''.join('<li>'+e(f)+'</li>' for f in row['facts'])+'</ul>'
        return [('Güzergâh ve konum bilgisi',facts+'<p>'+e(row['guidance'])+'</p>'+source_note(row['sources']))]
    return []
