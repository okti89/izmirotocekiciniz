"""Editoryal kapsam ve metin benzerliği incelemesi; Google sıralama testi değildir."""
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
from itertools import combinations
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from editorial_content import all_briefs
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def plain(html):
 p=Text();p.feed(html);return ' '.join(p.parts)
def tokens(text):return re.findall(r'[a-zçğıöşü]+',text.lower())
def grams(text):
 words=tokens(text);return {' '.join(words[i:i+4]) for i in range(len(words)-3)}
manifest=json.loads((ROOT/'pages.json').read_text())['pages']
catalog=json.loads((ROOT/'region-catalog.json').read_text())['regions']
briefs=all_briefs();paths={row['path']for row in catalog}
assert set(briefs)==paths,('editorial coverage',len(briefs),len(paths),sorted(paths-set(briefs)))
paragraphs=defaultdict(set);scenarios={};entries=[];fingerprints={};vectors={};status_counts=defaultdict(int)
place_names=sorted({row['name'].lower()for row in catalog},key=len,reverse=True)
for item in catalog:
 path=item['path'];row=briefs[path];scenario=row.get('scenario',{})
 status_counts[row.get('status','unspecified')]+=1
 rendered=(ROOT/'dist'/path.strip('/')/'index.html').read_text()
 assert 'yapılmış bir işin kaydı değildir' in rendered,(path,'scenario disclaimer not rendered')
 assert 'id="ornek-senaryo"' in rendered,(path,'scenario missing in rendered page')
 assert all(scenario.get(k) for k in ['title','situation','assessment','delivery']),(path,'incomplete illustrative scenario')
 assert len(row.get('questions',[]))>=2,(path,'specific FAQ missing')
 assert len(row.get('sections',[]))>=3,(path,'three topic-specific explanatory sections missing')
 texts=[p for section in row['sections']for p in section['paragraphs']]
 texts += [scenario[k]for k in ['situation','assessment','delivery']]
 texts += [q['q']+' '+q['a']for q in row['questions']]
 for text in texts:
  clean=' '.join(text.lower().split())
  if len(tokens(clean))>=28:paragraphs[clean].add(path)
 body=' '.join(texts)
 assert not re.search(r'\b(taşıdık|ulaştık|kurtardık|müşterimiz|yaptığımız işlem)\b',body.lower()),(path,'historical service claim in illustrative content')
 fingerprint=' '.join(tokens(body));assert fingerprint not in fingerprints,(path,'identical editorial body',fingerprints.get(fingerprint));fingerprints[fingerprint]=path
 masked=body.lower()
 for name in place_names:masked=masked.replace(name,'yer')
 vectors[path]=grams(masked)
 scen=' '.join(scenario[k]for k in ['situation','assessment','delivery']);assert scen not in scenarios,(path,'duplicated scenario');scenarios[scen]=path
 entries.append({'path':path,'editorial_word_count':len(tokens(body)),'paragraphs':len(texts),'faq':len(row['questions']),'scenario_labeled':True,'research_status':row.get('status'),'source_count':len(row.get('sources',[]))})
duplicates=[{'paragraph':p,'paths':sorted(v)} for p,v in paragraphs.items()if len(v)>1]
assert not duplicates,('long duplicated paragraph',duplicates[:3])
near=[]
for a,b in combinations(sorted(vectors),2):
 left,right=vectors[a],vectors[b];union=left|right
 score=len(left&right)/len(union)if union else 0
 if score>=.28:near.append({'paths':[a,b],'masked_4gram_jaccard':round(score,3)})
near.sort(key=lambda item:item['masked_4gram_jaccard'],reverse=True)
service_cases=json.loads((ROOT/'service_scenarios.json').read_text())
assert len(service_cases)==8
service_fingerprints=set()
for slug,case in service_cases.items():
 assert all(case.get(k)for k in ['title','situation','assessment','delivery']),(slug,'incomplete service scenario')
 body=' '.join(case[k]for k in ['situation','assessment','delivery'])
 assert body not in service_fingerprints,(slug,'duplicate service scenario')
 service_fingerprints.add(body)
 rendered=(ROOT/'dist/hizmetler'/slug/'index.html').read_text()
 assert 'yapılmış bir işin kaydı değildir' in rendered,(slug,'service scenario disclaimer missing')
report={'service_scenarios':len(service_fingerprints),'reviewed_on':'2026-10-11','scope':'Bölge sayfalarının özel editoryal bölümleri, örnek senaryolar ve FAQ. Menü, iletişim, kaynak notu ve adres tablosu benzerlik karşılaştırmasına katılmaz.','limitations':'Metin benzerliği özgünlük için yardımcı kontroldür; kapsamlılık, doğruluk veya Google sıralamasını tek başına kanıtlamaz. Senaryolar kurmacadır; gerçek iş kaydı değildir.','content_pages':len([p for p in manifest if p['path']!='/404/']),'research_status_counts':dict(status_counts),'region_briefs':len(entries),'unique_scenarios':len(scenarios),'duplicate_long_paragraphs':duplicates,'pairs_needing_editorial_review':near,'pages':entries}
(ROOT/'reports/unique-content-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'research_status_counts':dict(status_counts),'region_briefs':len(entries),'unique_scenarios':len(scenarios),'duplicate_long_paragraphs':len(duplicates),'review_pairs':len(near),'minimum_editorial_words':min(p['editorial_word_count']for p in entries)},ensure_ascii=False))
