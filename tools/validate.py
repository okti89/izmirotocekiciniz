from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,xml.etree.ElementTree as ET,argparse
ROOT=Path(__file__).resolve().parents[1]
args=argparse.ArgumentParser();args.add_argument('--directory',default=str(ROOT/'dist'));args.add_argument('--public',action='store_true');opt=args.parse_args();DIST=Path(opt.directory)
class P(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.ids=set();self.schemas=[];self.schema=False;self.meta={};self.canonical=None;self.title='';self.in_title=False;self.in_main=False;self.main=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if t=='title':self.in_title=True
  if t=='main':self.in_main=True
  if d.get('id'):self.ids.add(d['id'])
  if t in ('a','link','img','script'):
   link=d.get('href',d.get('src',''))
   if link.startswith('/'):self.links.append(link)
  if t=='meta':self.meta[d.get('name',d.get('property',''))]=d.get('content','')
  if t=='link'and d.get('rel')=='canonical':self.canonical=d.get('href')
  if t=='script'and d.get('type')=='application/ld+json':self.schema=True
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='main':self.in_main=False
  if t=='script':self.schema=False
 def handle_data(self,s):
  if self.in_title:self.title+=s
  if self.schema:self.schemas.append(s)
  if self.in_main and s.strip():self.main.append(s.strip())
manifest=json.loads((ROOT/'pages.json').read_text());plan=json.loads((ROOT/'publication-plan.json').read_text());mapping=json.loads((ROOT/'url-mapping.json').read_text());pages=manifest['pages'];assert len(pages)==len({p['path'] for p in pages});assert len(mapping['reference_mapping'])==275
expected_paths={p['path']for p in pages};parsed={};titles=set();descriptions=set();content=set()
for p in pages:
 path=p['path'];file=DIST/(path.strip('/')+'/index.html'if path!='/'else 'index.html');parser=P();parser.feed(file.read_text());parsed[path]=parser
 assert parser.h1==1,(path,'H1');assert parser.title not in titles,(path,'duplicate title');titles.add(parser.title)
 assert parser.meta['description']not in descriptions,(path,'duplicate description');descriptions.add(parser.meta['description'])
 assert parser.canonical=='https://izmirotocekiciniz.com'+path,(path,parser.canonical)
 assert parser.meta['og:url']==parser.canonical
 assert parser.meta['robots']==('index,follow'if opt.public and p['ready']else 'noindex,follow'),path
 for raw in parser.schemas:json.loads(raw)
 body=' '.join(parser.main);assert body not in content,(path,'duplicate complete body');content.add(body)
for path,p in parsed.items():
 for link in p.links:
  target,_,anchor=link.partition('#');file=DIST/target.lstrip('/');file=file/'index.html'if target.endswith('/')else file
  assert file.exists(),(path,'missing local target',link)
  if anchor:
   dest=parsed.get(target)
   assert dest and anchor in dest.ids,(path,'missing fragment',link)
for source,target in mapping['reference_mapping'].items():assert target in expected_paths,(source,target)
for source,target in mapping['redirects'].items():assert target in expected_paths and source!=target,(source,target)
sitemap=ET.parse(DIST/'sitemap.xml');urls={x.text for x in sitemap.getroot().iter()if x.tag.endswith('}loc')}
expected={'https://izmirotocekiciniz.com'+p for p in plan['phase_one']}if opt.public else set();assert urls==expected
phase_sitemap=ET.parse(ROOT/'launch/sitemap.xml');assert {x.text for x in phase_sitemap.getroot().iter()if x.tag.endswith('}loc')}=={'https://izmirotocekiciniz.com'+p for p in plan['phase_one']}
assert len(list(DIST.rglob('index.html')))==len(pages),'Untracked old output'
assert len(plan['phase_one'])==len([p for p in pages if p['path']!='/404/'])
assert not plan['phase_two']
assert '/404/' not in plan['phase_one']
assert ('X-Robots-Tag: noindex' in (DIST/'_headers').read_text())is(not opt.public)
print(json.dumps({'routes':len(pages),'content_pages':len(pages)-1,'indexable_pages':len(expected),'reference_urls_mapped':len(mapping['reference_mapping']),'validations':['unique titles and descriptions','single H1','domain canonical and Open Graph','schema JSON','internal links and fragments','all reference destinations','redirect targets','complete sitemap','noindex policy','no stale output']},ensure_ascii=False))
