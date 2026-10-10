"""Sayfa başına ayrı editoryal metin, kaynak ve açıkça etiketli örnek durumlar."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).parent
FILES=['research-district-briefs.json','research-route-briefs.json','research-remaining-places.json','research-neighborhood-briefs-a.json','research-neighborhood-briefs-b.json','research-neighborhood-briefs-c.json']

def read_records(filename):
    data=json.loads((ROOT/filename).read_text())
    for key in ['pages','regions','districts','places','neighborhoods','briefs']:
        if isinstance(data.get(key),dict):return data[key]
    return {key:value for key,value in data.items() if key.startswith('/')}

def all_briefs():
    out={}
    for filename in FILES:
        if (ROOT/filename).exists():
            for path,row in read_records(filename).items():
                assert path not in out,(filename,path,'overlapping brief')
                clean=dict(row)
                clean['sections']=[{'heading':section.get('heading',section.get('title','')),'paragraphs':section.get('paragraphs',[])} for section in row.get('sections',[])]
                clean['questions']=[{'q':q.get('q',q.get('question','')),'a':q.get('a',q.get('answer',''))} for q in row.get('questions',row.get('faq',[]))]
                clean.setdefault('status','supported_editorial_brief')
                out[path]=clean
    return out

def paragraphs(values):
    return ''.join('<p>'+e(text)+'</p>' for text in values if text)

def scenario_html(row):
    if not row:return ''
    return ('<section class="scenario" id="ornek-senaryo"><span class="scenario-label">ÖRNEK SENARYO</span><h2>'+e(row['title'])+'</h2>'
        '<p class="scenario-note">Bu örnek, hizmet planlamasını açıklamak için hazırlanmıştır; yapılmış bir işin kaydı değildir.</p>'
        '<h3>Durum</h3>'+paragraphs([row.get('situation','')])+
        '<h3>İlk değerlendirme</h3>'+paragraphs([row.get('assessment','')])+
        '<h3>Teslim planı</h3>'+paragraphs([row.get('delivery','')])+'</section>')

def brief_sections(row):
    sections=[]
    for section in row.get('sections',[]):
        texts=section.get('paragraphs',[])
        if isinstance(texts,str):texts=[texts]
        sections.append((section['heading'],paragraphs(texts)))
    return sections

def faq_html(row):
    questions=row.get('questions',[])
    if not questions:return ''
    return '<section><h2>Bu konum için sık sorulan sorular</h2><div class="faq">'+''.join('<details><summary>'+e(q['q'])+'</summary><p>'+e(q['a'])+'</p></details>' for q in questions)+'</div></section>'
