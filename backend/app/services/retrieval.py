import numpy as np,pandas as pd
from backend.app.config import INDEX,EMBEDDINGS
from backend.app.services.embedding import embed
class Store:
 def __init__(self): self.reload()
 def reload(self):
  self.ready=INDEX.exists() and EMBEDDINGS.exists()
  if self.ready:self.df=pd.read_csv(INDEX);self.vec=np.load(EMBEDDINGS)
 def search(self,text,k=5):
  if not self.ready:return []
  q=embed([text])[0]; scores=self.vec@q; ids=np.argsort(scores)[::-1][:k]
  return [{"case_name":str(self.df.iloc[i].get("case_name","Unknown")),"year":int(self.df.iloc[i].year),"similarity":round(float(scores[i]),4),"preview":str(self.df.iloc[i].get("preview",""))} for i in ids]
