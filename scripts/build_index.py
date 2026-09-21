import argparse,sys,re
from pathlib import Path
import pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from backend.app.config import INDEX,EMBEDDINGS
from backend.app.utils.pdf import extract_pdf
from backend.app.utils.text import clean,mask
from backend.app.services.embedding import embed
p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--limit',type=int);a=p.parse_args()
items=[]
for y in sorted(Path(a.dataset).iterdir()):
 if y.is_dir() and y.name.isdigit() and 1950<=int(y.name)<=2024:
  items += [(int(y.name),x) for x in y.glob('*.pdf')]
if a.limit:items=items[:a.limit]
rows=[];texts=[]
for n,(year,path) in enumerate(items,1):
 try:
  t=mask(clean(extract_pdf(path.read_bytes())))
  if len(t)<200:continue
  rows.append({'year':year,'case_name':re.sub(r'_+',' ',path.stem),'preview':t[:700],'source_file':str(path),'word_count':len(t.split())});texts.append(t[:12000])
 except Exception as e:print('Skipping',path.name,e)
print('Generating embeddings...');vec=embed(texts);INDEX.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(INDEX,index=False);np.save(EMBEDDINGS,vec);print('Indexed',len(rows),'cases')
