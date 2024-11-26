import time
from pdf2image import convert_from_path
from PIL import Image
import easyocr
import numpy as np
from multiprocessing import Pool

def process_page(page_num, image):
    result = {}
    try:
        print(f"\nProcessing Page {page_num}...")
        image_processing_start = time.time()
        image = image.convert('L')
        image_processing_end = time.time()
        image_processing_duration = image_processing_end - image_processing_start
        result['image_processing_duration'] = image_processing_duration

        image_save_path = f"processed_page_{page_num}.png"
        image.save(image_save_path)
        result['image_save_path'] = image_save_path

        image_np = np.array(image)

        ocr_start = time.time()
        reader = easyocr.Reader(['en'])
        text = reader.readtext(image_np)
        ocr_end = time.time()
        ocr_duration = ocr_end - ocr_start
        result['ocr_duration'] = ocr_duration

        result['text'] = text

    except Exception as e:
        result['error'] = str(e)

    return result

def main():
    start_time = time.time()

    pdf_path = "E:\\sample docs\\html cheatsheet.pdf"
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    first_page = 1
    last_page = 2

    pdf_conversion_start = time.time()
    images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page, poppler_path=poppler_path)
    pdf_conversion_end = time.time()
    pdf_conversion_duration = pdf_conversion_end - pdf_conversion_start
    print(f"PDF to Image Conversion Time: {pdf_conversion_duration:.4f} seconds")

  
    pool = Pool(processes=2)  
    results = []

    for page_num, image in enumerate(images, start=first_page):
        results.append(pool.apply_async(process_page, (page_num, image)))

   
    pool.close()
    pool.join()

 
    for result in results:
        page_result = result.get() 
        if 'error' in page_result:
            print(f"Error during OCR: {page_result['error']}")
        else:
            print(f"Image Processing Time (Pillow): {page_result['image_processing_duration']:.4f} seconds")
            print(f"Processed image saved as {page_result['image_save_path']}")
            print(f"OCR Time (easyocr): {page_result['ocr_duration']:.4f} seconds")
            # for item in page_result['text']:
            #     print(f"Detected Text: {item[1]} - Bounding Box: {item[0]}")

    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal Time for Processing: {total_duration:.4f} seconds")

if __name__ == "__main__":
    main()
