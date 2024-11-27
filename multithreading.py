import fitz  
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import time

def convert_pdf_to_image(pdf_path, page_number, resolution=2):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number - 1)  
        pix = page.get_pixmap(matrix=fitz.Matrix(resolution, resolution))  
        
     
        img_array = np.frombuffer(pix.samples, dtype=np.uint8)
        if img_array.size != pix.width * pix.height * pix.n:
            raise ValueError(f"Unexpected number of samples: expected {pix.width * pix.height * pix.n}, got {img_array.size}")
        
        img_array = img_array.reshape((pix.height, pix.width, pix.n))
        return img_array
    except Exception as e:
        print(f"Error converting PDF to image for page {page_number}: {e}")
        return None

def save_image(img_array, output_file):
    try:
        img = Image.fromarray(img_array)
        img.save(output_file)
        return f"Saved {output_file}"
    except Exception as e:
        print(f"Error saving image {output_file}: {e}")
        return None

def process_page(pdf_path, page_number, resolution=2):
    img_array = convert_pdf_to_image(pdf_path, page_number, resolution)
    if img_array is not None:
        output_file = f"page_{page_number}_processed.jpg"
        result = save_image(img_array, output_file)
        return result if result is not None else f"Failed to save page {page_number}"
    return f"Failed to process page {page_number}"
def process_page_wrapper(args):
    return process_page(*args)


if __name__ == "__main__":
    starttime = time.time()
    pdf_path = r"E:\sample docs\Iterations-codility.pdf"
    total_pages = 4  
    args = [(pdf_path, page_number) for page_number in range(1, total_pages + 1)]
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_page_wrapper, args))
    print("\n".join(results))
    endtime = time.time()
    print(f"\nTotal execution time: {endtime - starttime:.2f} seconds")