# import sys
# import easyocr
# from pdf2image import convert_from_path

# def ocr_image(image_path):
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(image_path)
#     for detection in result:
#         print(f"Detected Text: {detection[1]} - Bounding Box: {detection[0]}")

# def process_pdf(pdf_path, poppler_path):
#     images = convert_from_path(pdf_path, poppler_path=poppler_path)
#     for page_num, image in enumerate(images, start=1):
#         image_path = f"page_{page_num}.png"
#         image.save(image_path)
#         print(f"Processing Page {page_num}...")
#         ocr_image(image_path)

# if _name_ == "_main_":
#     pdf_path = r"D:\KIT\sem 2\beee qp2.pdf"
#     poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
#     process_pdf(pdf_path, poppler_path)

import easyocr
import multiprocessing
import time
def extract_text(image_path, lang):
    try:
        reader = easyocr.Reader([lang]) 
        result = reader.readtext(image_path)
        extracted_text = " ".join([text[1] for text in result])  
        print(f"Extracted Text from {image_path} in {lang}:")
        print(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"Error processing {image_path} in {lang}: {e}")
        return None

def process_image_parallel(image_path, languages):
    with multiprocessing.Pool(processes=len(languages)) as pool:
        results = pool.starmap(extract_text, [(image_path, lang) for lang in languages])
        pool.close()
        pool.join()
    return results
if __name__ == "__main__":

    image_path = "F:\Softcopy _official\Screenshot (191).png"
    languages = ['en', 'ta'] 

    start_time = time.time()
    extracted_texts = process_image_parallel(image_path, languages)

    print("\nTotal Execution Time:", time.time() - start_time)
    
    print("Starting script...") 
    print(f"Image Path: {image_path}")
    print(f"Languages: {languages}")
