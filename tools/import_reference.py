from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,time,re
ROOT=Path(__file__).resolve().parents[1]
class N:
 def __init__(self,tag='',attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[]
 def text(self):return ' '.join(' '.join(x.text() if isinstance(x,N) else x for x in self.children).split())
 def find(self,tag):
  out=[]
  for c in self.children:
   if isinstance(c,N):
    if c.tag==tag:out.append(c)
    out.extend(c.find(tag))
  return out
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.root=N();self.current=self.root
 def handle_starttag(self,t,a):
  n=N(t,a,self.current);self.current.children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.current=n
 def handle_endtag(self,t):
  n=self.current
  while n.parent and n.tag!=t:n=n.parent
  if n.tag==t and n.parent:self.current=n.parent
 def handle_data(self,s):self.current.children.append(s)
def extract(html,path):
 p=Parser();p.feed(html);r=p.root;h1=r.find('h1');heading=h1[0].text() if h1 else ''
 first=h1[0] if h1 else None
 while first and first.tag!='section':first=first.parent
 hero_paragraphs=[x.text() for x in first.find('p')] if first else []
 intro=hero_paragraphs[0] if hero_paragraphs else ''
 parent_links=[{'label':x.text(),'path':x.attrs.get('href','')}for x in first.find('a') if '-cekici' in x.attrs.get('href','')]if first else []
 features=[];neighborhoods=[]
 for section in r.find('section'):
  h=section.find('h3')
  if any('Yoğun Müdahale Arterleri' in x.text() for x in h):
   lists=section.find('ul')
   if lists:features=[x.text()for x in lists[0].find('li')]
   for heading_node in h:
    if 'Hizmet Verdiğimiz Mahalleler' in heading_node.text():neighborhoods=[x.text()for x in heading_node.parent.find('a')]
 crumbs=[]
 for nav in r.find('nav'):
  if nav.attrs.get('aria-label','').lower()=='breadcrumb':crumbs=[x.text()for x in nav.find('a')]
 localized=[]
 for section in r.find('section'):
  if 'Yerel konum ve hizmet planı' in section.text():
   localized=[x.text()for x in section.find('p') if 'Yerel adres kaydındaki yol adı:' in x.text()][:8]
 return {'revision':2,'reference_path':path,'heading':heading,'intro':intro,'hero_paragraphs':hero_paragraphs,'parent_links':parent_links,'roads':features,'neighborhoods':neighborhoods,'breadcrumbs':crumbs,'local_records':localized,'source_url':'https://izmircekicioto.com'+path}
items=json.loads((ROOT/'content-backlog.json').read_text())['regions'];output=ROOT/'reference-facts.json';existing={x['reference_path']:x for x in json.loads(output.read_text())}if output.exists()else {}
def work(item):
 path=item['reference_path']
 if path in existing and existing[path].get('revision')==2:return existing[path]
 for attempt in range(2):
  try:
   request=Request('https://izmircekicioto.com'+path,headers={'User-Agent':'Mozilla/5.0'})
   with urlopen(request,timeout=30)as response:
    result=extract(response.read().decode(),path);result['http_status']=response.status
   return result
  except Exception as ex:
   if attempt==1:return {'reference_path':path,'error':str(ex)}
   time.sleep(1)
results=[]
with ThreadPoolExecutor(max_workers=6)as pool:
 futures=[pool.submit(work,x)for x in items]
 for f in as_completed(futures):
  results.append(f.result())
  if len(results)%30==0:print(f'{len(results)}/{len(items)} reference pages read',flush=True)
output.write_text(json.dumps(sorted(results,key=lambda x:x['reference_path']),ensure_ascii=False,indent=2))
print(json.dumps({'pages':len(results),'errors':[x for x in results if x.get('error')],'missing_headings':[x['reference_path']for x in results if not x.get('heading')],'with_local_roads':sum(bool(x.get('roads'))for x in results)},ensure_ascii=False),flush=True)
