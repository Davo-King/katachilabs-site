import os,re,sys
from html.parser import HTMLParser
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=[];ids={}
for d,_,fs in os.walk(ROOT):
    if '/.git' in d or '/_' in d.replace(ROOT,''): continue
    for f in fs:
        if f.endswith('.html'): pages.append(os.path.join(d,f))
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=set()
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        for k in('href','src'):
            if k in a: s.refs.append((t,k,a[k]))
        if 'srcset' in a:
            for part in a['srcset'].split(','): s.refs.append((t,'srcset',part.strip().split()[0]))
        if t=='meta' and a.get('http-equiv')=='refresh': s.refs.append((t,'refresh',a['content'].split('url=')[1]))
def resolve(u):
    p=os.path.join(ROOT,u.lstrip('/'))
    if os.path.isdir(p): p=os.path.join(p,'index.html')
    return p
parsed={}
for pg in pages:
    p=P(); p.feed(open(pg,encoding='utf-8').read()); parsed[pg]=p
bad=0;n=0
for pg,p in parsed.items():
    rel=pg.replace(ROOT,'')
    pageurl='/'+os.path.relpath(pg,ROOT).replace('index.html','')
    for t,k,u in p.refs:
        if u.startswith(('mailto:','http://','https://','data:')): continue
        if u=='#': print(f'  note {rel}: placeholder href="#" ({t})'); continue
        n+=1
        path,_,frag=u.partition('#')
        if path=='' : target=pg
        elif not path.startswith('/'): print(f'  RELATIVE {rel}: {u}'); bad+=1; continue
        else: target=resolve(path)
        if not os.path.isfile(target): print(f'  BROKEN {rel}: {u}'); bad+=1; continue
        if frag and target in parsed and frag not in parsed[target].ids: print(f'  BAD ANCHOR {rel}: {u}'); bad+=1
print(f'{len(pages)} pages, {n} internal refs checked, {bad} problems')
for pg in pages: print('page:',pg.replace(ROOT,''))
