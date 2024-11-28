import time
from pdf2image import convert_from_path
from concurrent.futures import ProcessPoolExecutor
from typing import List
from io import BytesIO

def convert_pdf_page_to_bytes(pdf_path, page_number, dpi=300, poppler_path=None) -> BytesIO:
    try:
        images = convert_from_path(
            pdf_path, dpi=dpi, first_page=page_number, last_page=page_number, poppler_path=poppler_path
        )
        if not images:
            raise ValueError(f"Page {page_number} could not be converted.")
        byte_stream = BytesIO()
        images[0].save(byte_stream, format="PNG")
        byte_stream.seek(0)
        return byte_stream
    except Exception as e:
        print(f"Error converting page {page_number}: {e}")
        return None

def save_image_bytes(byte_stream: BytesIO, output_file: str):
    try:
        with open(output_file, "wb") as f:
            f.write(byte_stream.read())  
        return f"Saved {output_file}"
    except Exception as e:
        print(f"Error saving {output_file}: {e}")
        return None

def process_page(pdf_path, page_number, dpi=300, poppler_path="C:\\poppler\\bin"):
    byte_stream = convert_pdf_page_to_bytes(pdf_path, page_number, dpi, poppler_path)
    if byte_stream is not None:
        output_file = f"page_{page_number}_processed.png"
        result = save_image_bytes(byte_stream, output_file)
        return result if result is not None else f"Failed to save page {page_number}"
    return f"Failed to process page {page_number}"

def process_page_wrapper(args):
    return process_page(*args)

async def convert_pdf_to_io_bytes(pdf_path: bytes, dpi=300, poppler_path=None) -> List[BytesIO]:
    pdf_images = []
    try:
        images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        for image in images:
            byte_stream = BytesIO()
            image.save(byte_stream, format="PNG")
            byte_stream.seek(0)
            pdf_images.append(byte_stream)
    except Exception as e:
        print(f"Error processing PDF to bytes: {e}")
    return pdf_images

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
    

    starttime = time.time()
    results = []
    for page_number in range(1, total_pages + 1):
        result = process_page(pdf_path, page_number, dpi=300, poppler_path=poppler_path)
        results.append(result)
    
    print("\n".join(results))
    endtime = time.time()
    print(f"\nTotal execution time (single processor): {endtime - starttime:.2f} seconds")

import time
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from typing import List
from io import BytesIO

def convert_pdf_page_to_bytes(pdf_path, page_number, dpi=300, poppler_path=None) -> BytesIO:
    try:
        images = convert_from_path(
            pdf_path, dpi=dpi, first_page=page_number, last_page=page_number, poppler_path=poppler_path
        )
        if not images:
            raise ValueError(f"Page {page_number} could not be converted.")
        byte_stream = BytesIO()
        images[0].save(byte_stream, format="PNG")
        byte_stream.seek(0)
        return byte_stream
    except Exception as e:
        print(f"Error converting page {page_number}: {e}")
        return None

def save_image_bytes(byte_stream: BytesIO, output_file: str):
    try:
        with open(output_file, "wb") as f:
            f.write(byte_stream.read())  
        return f"Saved {output_file}"
    except Exception as e:
        print(f"Error saving {output_file}: {e}")
        return None

def process_page(pdf_path, page_number, dpi=300, poppler_path=None):
    byte_stream = convert_pdf_page_to_bytes(pdf_path, page_number, dpi, poppler_path)
    if byte_stream is not None:
        output_file = f"page_{page_number}_processed.png"
        result = save_image_bytes(byte_stream, output_file)
        return result if result is not None else f"Failed to save page {page_number}"
    return f"Failed to process page {page_number}"

def process_page_wrapper(args):
    return process_page(*args)

if __name__ == "__main__":
    pdf_path = r"E:\sample docs\Iterations-codility.pdf"
    total_pages = 4
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    args = [(pdf_path, page_number, 300, poppler_path) for page_number in range(1, total_pages + 1)]

    # Multiprocessing using ThreadPoolExecutor
    starttime = time.time()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_page_wrapper, args))
    print("\n".join(results))
    endtime = time.time()
    print(f"\nTotal execution time (multi-threaded): {endtime - starttime:.2f} seconds")

    # Single-threaded version
    starttime = time.time()
    results = []
    for page_number in range(1, total_pages + 1):
        result = process_page(pdf_path, page_number, dpi=300, poppler_path=poppler_path)
        results.append(result)
    print("\n".join(results))
    endtime = time.time()
    print(f"\nTotal execution time (single-threaded): {endtime - starttime:.2f} seconds")

import time
from pdf2image import convert_from_path
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
import os

def batch_convert_to_bytes(pdf_path, page_range, dpi=300, poppler_path=None):
    try:
        images = convert_from_path(
            pdf_path, dpi=dpi, first_page=page_range[0], last_page=page_range[1], poppler_path=poppler_path
        )
        byte_streams = []
        for i, image in enumerate(images, start=page_range[0]):
            byte_stream = BytesIO()
            image.save(byte_stream, format="PNG")
            byte_stream.seek(0)
            byte_streams.append((i, byte_stream))
        return byte_streams
    except Exception as e:
        return []

def save_image_from_bytes(page_number, byte_stream, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"page_{page_number}.png")
    try:
        with open(output_file, "wb") as f:
            f.write(byte_stream.read())
        return f"Saved {output_file}"
    except Exception as e:
        return f"Error saving page {page_number}: {e}"

def process_page_range(args):
    pdf_path, page_range, dpi, poppler_path = args
    results = []
    byte_streams = batch_convert_to_bytes(pdf_path, page_range, dpi, poppler_path)
    for page_number, byte_stream in byte_streams:
        results.append(save_image_from_bytes(page_number, byte_stream))
    return results

if __name__ == "__main__":
    pdf_path = r"E:\sample docs\Iterations-codility.pdf"
    total_pages = 10
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    page_ranges = [(i, min(i, total_pages)) for i in range(1, total_pages + 1)]

    # Single Processing
    starttime = time.time()
    results_single = []
    for page_range in page_ranges:
        results_single.extend(process_page_range((pdf_path, page_range, 300, poppler_path)))
    endtime = time.time()
    total_time_single = endtime - starttime
    avg_time_single = total_time_single / total_pages
    print("\n".join(results_single))
    print(f"\nTotal execution time (single processing): {total_time_single:.2f} seconds")
    print(f"Average time per page (single processing): {avg_time_single:.2f} seconds")

    # Multiprocessing
    starttime = time.time()
    with ProcessPoolExecutor() as executor:
        results_multi = list(executor.map(process_page_range, [(pdf_path, page_range, 300, poppler_path) for page_range in page_ranges]))
    results_multi_flat = [item for sublist in results_multi for item in sublist]
    endtime = time.time()
    total_time_multi = endtime - starttime
    avg_time_multi = total_time_multi / total_pages
    print("\n".join(results_multi_flat))
    print(f"\nTotal execution time (multiprocessing): {total_time_multi:.2f} seconds")
    print(f"Average time per page (multiprocessing): {avg_time_multi:.2f} seconds")
