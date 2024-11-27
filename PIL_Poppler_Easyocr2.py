import time
from pdf2image import convert_from_path
from PIL import Image
import easyocr
import numpy as np

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

for page_num, image in enumerate(images, start=first_page):
    print(f"\nProcessing Page {page_num}...")

    image_processing_start = time.time()
    image = image.convert('L')
    image_processing_end = time.time()
    image_processing_duration = image_processing_end - image_processing_start
    print(f"Image Processing Time (Pillow): {image_processing_duration:.4f} seconds")

    image_save_path = f"processed_page_{page_num}.png"
    image.save(image_save_path)
    print(f"Processed image saved as {image_save_path}")

    image_np = np.array(image)

    ocr_start = time.time()
    reader = easyocr.Reader(['en'])
    try:
        text = reader.readtext(image_np)
        ocr_end = time.time()
        ocr_duration = ocr_end - ocr_start
        print(f"OCR Time (easyocr): {ocr_duration:.4f} seconds")

        for item in text:
            print(f"Detected Text: {item[1]} - Bounding Box: {item[0]}")

    except Exception as e:
        print(f"Error during OCR: {e}")
        continue

end_time = time.time()
total_duration = end_time - start_time
print(f"\nTotal Time for Processing: {total_duration:.4f} seconds")






