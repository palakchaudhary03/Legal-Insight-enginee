import re
from collections import Counter

STOP={"the","and","that","this","with","from","were","have","has","been","shall","would","could","there","their","which","where","while","about","into","after","before","under","over","such","also","case","court","state","section","order","said","upon"}

# Indian Kanoon running header: "<case name> on <date> Indian Kanoon - <url> <page num>"
HEADER_RE = re.compile(
    r"[^.]{0,150}?\bon\s+\d{1,2}\s+\w+,?\s+\d{4}\s+Indian Kanoon\s*-\s*https?://\S+\s*\d{0,3}",
    re.IGNORECASE
)

def clean(t):
    t = t.replace("\xa0", " ")
    t = HEADER_RE.sub(" ", t)              # remove repeated Indian Kanoon header/citation
    t = re.sub(r"https?://\S+", " ", t)    # remove any leftover URLs
    return re.sub(r"\s+", " ", t).strip()

def mask(t):
    t=re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b","[EMAIL]",t)
    t=re.sub(r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b","[PHONE]",t)
    return re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b","[ID_NUMBER]",t)

def summary(t,n=5):
    s=[x.strip() for x in re.split(r"(?<=[.!?])\s+",t) if len(x.strip())>50]
    if not s:return "No readable summary could be generated."
    f=Counter(w for w in re.findall(r"[A-Za-z]{4,}",t.lower()) if w not in STOP)
    ranked=[]
    for i,x in enumerate(s): ranked.append((sum(f[w] for w in re.findall(r"[A-Za-z]{4,}",x.lower())),i,x))
    return " ".join(x[2] for x in sorted(sorted(ranked,reverse=True)[:n],key=lambda z:z[1]))

def terms(t,n=10):
    f=Counter(w for w in re.findall(r"[A-Za-z]{5,}",t.lower()) if w not in STOP)
    return [w for w,_ in f.most_common(n)]