from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.utils.pdf import extract_pdf
from backend.app.utils.text import clean,mask,summary,terms
from backend.app.services.retrieval import Store
from backend.app.config import INDEX,EMBEDDINGS,MAX_MB
app=FastAPI(title="Legal Insight Engine")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
store=Store()
@app.get("/api/health")
def health():return {"status":"ok","index_ready":store.ready}
@app.get("/api/stats")
def stats():
 if not store.ready:return {"index_ready":False,"cases":0,"years":0,"start_year":1950,"end_year":2024}
 return {"index_ready":True,"cases":len(store.df),"years":store.df.year.nunique(),"start_year":int(store.df.year.min()),"end_year":int(store.df.year.max())}
@app.post("/api/analyze")
async def analyze(file:UploadFile=File(...)):
 if not file.filename.lower().endswith('.pdf'):raise HTTPException(400,'Please upload a PDF file.')
 data=await file.read()
 if len(data)>MAX_MB*1024*1024:raise HTTPException(400,f'File is larger than {MAX_MB} MB.')
 try:
  text=mask(clean(extract_pdf(data)))
  return {"summary":summary(text),"key_terms":terms(text),"word_count":len(text.split()),"similar_cases":store.search(text,20)}
 except Exception as e:raise HTTPException(500,str(e))
