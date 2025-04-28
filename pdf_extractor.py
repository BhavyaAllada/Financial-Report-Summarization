# pdf_extractor.py
import fitz  
import os

def extract_text_from_pdf(file_path: str) -> str:
    """Extract full text from a PDF file using PyMuPDF."""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Failed to extract {file_path}: {e}")
    return text

def read_all_pdfs_from_folder(folder_path: str) -> dict:
    """Reads all PDFs from a folder and returns a dictionary {filename: content}."""
    pdf_texts = {}
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            pdf_texts[file_name] = extract_text_from_pdf(full_path)
    return pdf_texts

# Sample usage
if __name__ == "__main__":
    folder = "./data/input_reports"  
    all_pdfs_content = read_all_pdfs_from_folder(folder)
    
    for filename, content in all_pdfs_content.items():
        print(f"\n--- {filename} ---\n")
        print(content[:1000])  # Print first 1000 characters
