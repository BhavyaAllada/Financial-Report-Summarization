import os
import fitz  
import json
import shutil

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")  
    return text

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    img_list = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_filename = f"image_{page_num + 1}_{xref}.png"
            img_filepath = os.path.join(output_folder, img_filename)
            with open(img_filepath, "wb") as img_file:
                img_file.write(image_bytes)
            img_list.append(img_filepath)
    return img_list

def extract_tables_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    tables = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        rows = text.split("\n")
        for row in rows:
            columns = row.split()
            if len(columns) > 1:  
                tables.append(columns)
    return tables

def process_pdfs(input_folder, output_folder):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    extracted_data = {}

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        print(f"Processing: {pdf_file}")
        
        pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
        os.makedirs(pdf_output_folder, exist_ok=True)
        
        text = extract_text_from_pdf(pdf_path)
        
        images = extract_images_from_pdf(pdf_path, pdf_output_folder)
        
        tables = extract_tables_from_pdf(pdf_path)

        extracted_data[pdf_file] = {
            "text": text,
            "images": images,
            "tables": tables
        }

    return extracted_data

if __name__ == "__main__":
    input_folder = "data/input_reports"
    output_folder = "data/output_docs"
    
    os.makedirs(output_folder, exist_ok=True)
    
    extracted_data = process_pdfs(input_folder, output_folder)
    
    with open(os.path.join(output_folder, "extracted_data.json"), "w") as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print("Extraction completed!")
