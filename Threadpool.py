import concurrent.futures
from tqdm import tqdm
import fitz

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

def process_pdf_in_parallel(pdf_paths):
    NTHREADS = 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=NTHREADS) as executor:
        results = list(tqdm(executor.map(extract_text_from_pdf, pdf_paths), total=len(pdf_paths)))
    return results

pdf_files = [
    "D:/KIT/AI for urban countries.pdf", 
    "D:/KIT/Resume/Muralidharan CV resume.pdf", 
    "D:/KIT/B.Tech.AIDS.pdf"
]

processed_data = process_pdf_in_parallel(pdf_files)

for idx, data in enumerate(processed_data):
    print(f"--- Extracted text from PDF {idx + 1} ---")
    print(data[:500])
    print("\n" + "-"*40 + "\n")
