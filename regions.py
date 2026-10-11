
"""Bölge sayfaları: kaynaklı konum bilgisi ve ayrı editoryal rehberler."""
from pathlib import Path
from html import escape as e
from urllib.parse import quote
import json,re
from local_content import region_sections
from editorial_content import all_briefs,brief_sections,scenario_html,faq_html
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
 catalog=[];mapping={'/izmir-cekici':'/'};briefs=all_briefs()
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
  # Eski URL korunur; resmî muhtarlık kaydı Liman Reis'i Narlıdere ile eşler.
  if stem=='liman-reis':district,candidates='Narlıdere',['Narlıdere']
  brief=briefs.get(path,{})
  if brief.get('status') in ('verified','verified_correction') and brief.get('district'):
   district,candidates=brief['district'],[brief['district']]
  if brief.get('status') in ('ambiguous','unresolved','outside_izmir'):
   district,candidates=None,[]
  roads=list(dict.fromkeys(y for x in valid for y in x.get('roads',[])))
  catalog.append({'name':name,'path':path,'kind':kind,'district':district,'candidates':candidates,'roads':roads,'source_note':record.get('hero_paragraphs',[''])[-1],'source_paths':group['references'],'stem':stem})
  for source in group['references']:mapping[source]=path
 assert len({x['path']for x in catalog})==len(catalog),'Canonical path collision'
 return catalog,mapping

def render_regions(root,layout,subhero,buttons,ORIGIN,PUBLIC):
 catalog,mapping=build_region_catalog(root);approved=set(json.loads((root/'index-regions.json').read_text())['indexable_paths']);assert approved <= {x['path'] for x in catalog};by_path={x['path']:x for x in catalog};by_name={x['name']:x for x in catalog}
 briefs=all_briefs()
 for item in catalog:
  name=item['name'];path=item['path'];district=item['district'];kind=item['kind'];stem=item['stem']
  parent_path='/bolgeler/'+slug(district)+'/'if district and district!=name else '/hizmet-bolgeleri/'
  parent_name=district+' çekici'if district and district!=name else 'Hizmet bölgeleri'
  desc=f'{name} için 7/24 çekici ve yol yardım talebi. '+(f'{district} bağlantılı konum ve erişim bilgileri. 'if district and district!=name else '')+'0536 676 28 66 üzerinden araç bilgisi ve konumunuzu paylaşın.'
  brief=briefs.get(path,{})
  sections=region_sections(item)+brief_sections(brief)
  request='Merhaba, '+name+' için çekici/yol yardım talebim var.\nİlçe ve tam konum: \nAraç marka-modeli: \nSorun ve hareket durumu: \nTeslim adresi: '
  wa='https://wa.me/905366762866?text='+quote(request)
  local_body=''.join(f'<section><h2>{e(h)}</h2><div class="region-copy">{t}</div></section>'for h,t in sections)
  local_body+=scenario_html(brief.get('scenario'))+faq_html(brief)
  related=[]
  if district and district!=name:related.append((district+' çekici',parent_path))
  if kind=='ilceler':related+=[(x['name']+' çekici',x['path'])for x in catalog if x['district']==name and x['kind']=='noktalar'][:24]
  elif item['candidates']:related+=[(d+' çekici','/bolgeler/'+slug(d)+'/')for d in item['candidates']if d!=district]
  if related:local_body+='<section><h2>İlgili bölge sayfaları</h2><ul class="related-links">'+''.join(f'<li><a href="{p}">{e(n)}</a></li>'for n,p in related)+'</ul></section>'
  local_body+='<section><h2>İhtiyacınızla ilgili hizmet rehberleri</h2><ul class="related-links"><li><a href="/hizmetler/oto-cekici/">Oto çekici ve servis transferi</a></li><li><a href="/hizmetler/aku-takviye/">Akü takviye</a></li><li><a href="/hizmetler/motosiklet-cekici/">Motosiklet taşıma</a></li><li><a href="/hizmetler/oto-kurtarma/">Kurtarma ihtiyacı</a></li></ul></section>'
  aside=f'<aside class="aside"><span class="eyebrow">7/24 TALEP HATTI</span><h3>{e(name)} için bize ulaşın.</h3><p>Ücret ve tahmini varış, gerçek konumunuz ve araç durumuyla görüşmede belirlenir.</p><a class="btn" href="tel:+905366762866">0536 676 28 66</a><a class="btn secondary" href="{wa}">WhatsApp ile yazın</a><p style="margin-top:20px">İzmir geneli hizmet. Ekip ve mesafe uygunluğu gerçek konumunuza göre değerlendirilir.</p><a class="text-link" href="/fiyatlandirma/">Ücretlendirme bilgisi</a></aside>'
  page_heading=name+' çekici ve yol yardım'
  if brief.get('status')=='outside_izmir':
   page_heading=name+'–İzmir araç transferi talebi';desc=name+' ile İzmir arasındaki araç transferi talebinde alınış ve teslim illerini ayrı belirtin. Hizmet uygunluğu, kapsam ve ücret görüşmede değerlendirilir.'
  body=subhero(page_heading,desc,path,(parent_name,parent_path))+'<section class="section"><div class="wrap detail-grid"><article class="article">'+local_body+'</article>'+aside+'</div></section>'
  layout(path,page_heading+' | İzmir Oto Çekiciniz',desc,body,ready=path in approved,crumbs=[('Ana sayfa','/'),(parent_name,parent_path),(name+' çekici',path)],service=page_heading,area='İzmir' if brief.get('status')=='outside_izmir' else name,faqs=brief.get('questions'))
 (root/'region-catalog.json').write_text(json.dumps({'regions':catalog,'reference_url_mapping':mapping},ensure_ascii=False,indent=2))
 return catalog,mapping
