import time
from pdf2image import convert_from_path
from concurrent.futures import ProcessPoolExecutor

def convert_pdf_page_to_image(pdf_path, page_number, dpi=300, poppler_path=None):
    try:
        images = convert_from_path(
            pdf_path, dpi=dpi, first_page=page_number, last_page=page_number, poppler_path=poppler_path
        )
        if not images:
            raise ValueError(f"Page {page_number} could not be converted.")
        return images[0]  # Return the PIL Image object directly
    except Exception as e:
        print(f"Error converting page {page_number}: {e}")
        return None

def save_image(img, output_file):
    try:
        img.save(output_file, format="PNG")  # Save the image directly to file
        return f"Saved {output_file}"
    except Exception as e:
        print(f"Error saving {output_file}: {e}")
        return None

def process_page(pdf_path, page_number, dpi=300, poppler_path="C:\\poppler\\bin"):
    img = convert_pdf_page_to_image(pdf_path, page_number, dpi, poppler_path)
    if img is not None:
        output_file = f"page_{page_number}_processed.png"
        result = save_image(img, output_file)
        return result if result is not None else f"Failed to save page {page_number}"
    return f"Failed to process page {page_number}"

def process_page_wrapper(args):
    return process_page(*args)

if __name__ == "__main__":
    starttime = time.time()
    pdf_path = r"E:\sample docs\Iterations-codility.pdf"
    total_pages = 4
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    args = [(pdf_path, page_number, 300, poppler_path) for page_number in range(1, total_pages + 1)]
    
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_page_wrapper, args))
    
    print("\n".join(results))
    endtime = time.time()
    print(f"\nTotal execution time (multiprocessor): {endtime - starttime:.2f} seconds")


# import time
# from pdf2image import convert_from_path

# def convert_pdf_page_to_image(pdf_path, page_number, dpi=300, poppler_path=None):
#     try:
#         images = convert_from_path(
#             pdf_path, dpi=dpi, first_page=page_number, last_page=page_number, poppler_path=poppler_path
#         )
#         if not images:
#             raise ValueError(f"Page {page_number} could not be converted.")
#         return images[0]  # Return the PIL Image object directly
#     except Exception as e:
#         print(f"Error converting page {page_number}: {e}")
#         return None

# def save_image(img, output_file):
#     try:
#         img.save(output_file, format="PNG")  # Save the image directly to file
#         return f"Saved {output_file}"
#     except Exception as e:
#         print(f"Error saving {output_file}: {e}")
#         return None

# def process_page(pdf_path, page_number, dpi=300, poppler_path="C:\\poppler\\bin"):
#     img = convert_pdf_page_to_image(pdf_path, page_number, dpi, poppler_path)
#     if img is not None:
#         output_file = f"page_{page_number}_processed.png"
#         result = save_image(img, output_file)
#         return result if result is not None else f"Failed to save page {page_number}"
#     return f"Failed to process page {page_number}"

# if __name__ == "__main__":
#     starttime = time.time()
#     pdf_path = r"E:\sample docs\Iterations-codility.pdf"
#     total_pages = 4
#     poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
#     results = []
    
#     for page_number in range(1, total_pages + 1):
#         result = process_page(pdf_path, page_number, dpi=300, poppler_path=poppler_path)
#         results.append(result)
    
#     print("\n".join(results))
#     endtime = time.time()
#     print(f"\nTotal execution time (single processor): {endtime - starttime:.2f} seconds")
