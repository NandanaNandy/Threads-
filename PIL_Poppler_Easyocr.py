from PIL import Image
import easyocr
import sys
from pdf2image import convert_from_path
import os
import numpy as np
ROOT_DIR = os.path.abspath(os.curdir)
PDF_file = ROOT_DIR + r"\sample docs\html cheatsheet.pdf"
try:
    pages = convert_from_path(PDF_file, 500, poppler_path=r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin")
except Exception as e:
    print(f"Error converting PDF to images: {e}")
    sys.exit(1)
reader = easyocr.Reader(['en']) 
for i, page in enumerate(pages):
    try:
        page_np = np.array(page)
        
        
        text = reader.readtext(page_np)
        
        print(f"Text from page {i+1}:")
        for detection in text:
            print(f"Detected text: {detection[1]} (Position: {detection[0]})")
    except Exception as e:
        print(f"Error processing page {i+1}: {e}")
    

    page.save(f"page_{i+1}.png", 'PNG')
