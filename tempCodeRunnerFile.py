from PIL import Image
import easyocr
import sys
from pdf2image import convert_from_path
import os

ROOT_DIR = os.path.abspath(os.curdir)
PDF_file = ROOT_DIR + r"\sample docs\html cheatsheet.pdf"

# Step 1: Convert PDF to images
try:
    pages = convert_from_path(PDF_file, 500, poppler_path=r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin")
except Exception as e:
    print(f"Error converting PDF to images: {e}")
    sys.exit(1)

# Step 2: Initialize EasyOCR reader
reader = easyocr.Reader(['en']) 

# Step 3: OCR on each page
for i, page in enumerate(pages):
    try:
        text = reader.readtext(page)
        print(f"Text from page {i+1}:")
        for detection in text:
            print(f"Detected text: {detection[1]} (Position: {detection[0]})")
    except Exception as e:
        print(f"Error processing page {i+1}: {e}")
    
    # Save the page image as PNG
    page.save(f"page_{i+1}.png", 'PNG')
