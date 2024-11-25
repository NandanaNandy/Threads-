import concurrent.futures
import multiprocessing
from poppler import load_from_file, PageRenderer
import easyocr
from tqdm import tqdm

def extract_images_from_pdf(pdf_path):
    pdf_document = load_from_file(pdf_path)
    page_renderer = PageRenderer()
    images = []
    
    for i in range(len(pdf_document)):
        page = pdf_document.create_page(i)
        image = page_renderer.render_page(page)
        images.append(image)
    
    return images

def ocr_on_image(image):
    reader = easyocr.Reader(['en'])
    return reader.readtext(image)

def process_pdf(pdf_path):
    images = extract_images_from_pdf(pdf_path)
    ocr_results = []
    
    for image in images:
        ocr_results.append(ocr_on_image(image))
    
    return ocr_results

def process_pdfs_in_parallel(pdf_paths):
    NCPU = multiprocessing.cpu_count() - 2 
    NTHREADS = 4 

    with multiprocessing.Pool(processes=NCPU) as pool:
        results = list(tqdm(pool.imap(process_pdf, pdf_paths), total=len(pdf_paths)))
    
    return results


pdf_files = [
    "D:/KIT/AI for urban countries.pdf", 
    "D:/KIT/Resume/Muralidharan CV resume.pdf", 
    "D:/KIT/B.Tech.AIDS.pdf"
]
processed_data = process_pdfs_in_parallel(pdf_files)
