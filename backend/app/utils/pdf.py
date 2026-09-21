import fitz
def extract_pdf(data:bytes)->str:
    doc=fitz.open(stream=data,filetype="pdf")
    try:return "\n".join(p.get_text() for p in doc)
    finally:doc.close()
