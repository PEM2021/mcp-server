from PyPDF2 import PdfReader

def extract_resume_text(pdf_path: str = "resume.pdf") -> str:
    reader = PdfReader(pdf_path)
    return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
