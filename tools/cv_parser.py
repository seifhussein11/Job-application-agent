import fitz

from docx import Document

def parse_pdf(pdf_path):
    
    doc = fitz.open(pdf_path)
    
    text = ""
    
    for page in doc:
        print(page.get_text())
        text+= page.get_text()
        
    doc.close()
    
    return text.strip()


def parse_docx(docx_path):
    
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()


def parse_CV(file_path):
    
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    
    else:
        raise ValueError("Unsupported file type")