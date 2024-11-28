import time
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
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

    starttime = time.time()
    results_single = []
    for page_range in page_ranges:
        results_single.extend(process_page_range((pdf_path, page_range, 300, poppler_path)))
    endtime = time.time()
    print("\n".join(results_single))
    print(f"\nTotal execution time (single processing): {endtime - starttime:.2f} seconds")

    starttime = time.time()
    with ProcessPoolExecutor() as executor:
        results_multi = list(executor.map(process_page_range, [(pdf_path, page_range, 300, poppler_path) for page_range in page_ranges]))
    results_multi_flat = [item for sublist in results_multi for item in sublist]
    endtime = time.time()
    print("\n".join(results_multi_flat))
    print(f"\nTotal execution time (multiprocessing): {endtime - starttime:.2f} seconds")
