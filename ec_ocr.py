import sys
import easyocr
from pdf2image import convert_from_path

def ocr_image(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    for detection in result:
        print(f"Detected Text: {detection[1]} - Bounding Box: {detection[0]}")

def process_pdf(pdf_path, poppler_path):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for page_num, image in enumerate(images, start=1):
        image_path = f"page_{page_num}.png"
        image.save(image_path)
        print(f"Processing Page {page_num}...")
        ocr_image(image_path)

if _name_ == "_main_":
    pdf_path = r"D:\KIT\sem 2\beee qp2.pdf"
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    process_pdf(pdf_path, poppler_path)