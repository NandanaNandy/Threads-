import multiprocessing
import os
import time
from poppler import load_from_file, PageRenderer

def process_pdf(file_path):
    try:
        start_time = time.time()
        pdf_document = load_from_file(file_path)
        page_count = pdf_document.pages
        renderer = PageRenderer()
        output_dir = "output_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for page_number in range(page_count):
            page = pdf_document.create_page(page_number)
            image = renderer.render_page(page)
            image_name = os.path.join(output_dir, f"{os.path.basename(file_path)}_page_{page_number + 1}.png")
            image.save(image_name, "png")
        end_time = time.time()
        return f"Processed {file_path} with {page_count} pages in {end_time - start_time:.2f} seconds"
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def main():
    pdf_directory = "E:\sample docs"
    pdf_files = [os.path.join(pdf_directory, file) for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    num_processes = multiprocessing.cpu_count()

    start_time = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_pdf, pdf_files)
    end_time = time.time()

    for result in results:
        print(result)
    
    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()




