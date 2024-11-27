from typing import List
from io import BytesIO
import time
from pdf2image import convert_from_path
import easyocr
import multiprocessing


async def convert_pdf_to_io_bytes(pdf_path: str, dpi: int = 300, fmt: str = "png", poppler_path: str = None) -> List[BytesIO]:
    images = convert_from_path(pdf_path, dpi=dpi, fmt=fmt, poppler_path=poppler_path)
    buffer_list = []
    for image in images:
        buffer = BytesIO()
        image.save(buffer, format=fmt)
        buffer.seek(0)
        buffer_list.append(buffer)
    return buffer_list


def ocr_image(image_stream: BytesIO, languages: List[str] = ["en"]) -> str:
    image_stream.seek(0)
    reader = easyocr.Reader(languages)
    result = reader.readtext(image_stream)
    return " ".join([text[1] for text in result])


def process_pdf_single(pdf_path: str, languages: List[str] = ["en"], **kwargs) -> List[str]:
    buffers = asyncio.run(convert_pdf_to_io_bytes(pdf_path, **kwargs))
    results = [ocr_image(buffer, languages) for buffer in buffers]
    return results


def process_pdf_multi(pdf_path: str, languages: List[str] = ["en"], **kwargs) -> List[str]:
    buffers = asyncio.run(convert_pdf_to_io_bytes(pdf_path, **kwargs))
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(ocr_image, [(buffer, languages) for buffer in buffers])
    return results


def benchmark(function, *args, iterations: int = 10, **kwargs) -> float:
    times = []
    for _ in range(iterations):
        start_time = time.time()
        function(*args, **kwargs)
        times.append(time.time() - start_time)
    return sum(times) / len(times)



if __name__ == "__main__":
    import asyncio
    pdf_path = r"E:\sample docs\Iterations-codility.pdf"
    poppler_path = r"E:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    avg_time_single = benchmark(process_pdf_single, pdf_path, languages=["en", "ta"], poppler_path=poppler_path)
    print(f"Average time (single-process): {avg_time_single:.2f} seconds")
    avg_time_multi = benchmark(process_pdf_multi, pdf_path, languages=["en", "ta"], poppler_path=poppler_path)
    print(f"Average time (multi-process): {avg_time_multi:.2f} seconds")
