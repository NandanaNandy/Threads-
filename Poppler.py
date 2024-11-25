import multiprocessing
from poppler import load_from_file, PageRenderer

def process_pdf(pdf_path):
    pdf_document = load_from_file(pdf_path)
    page_1 = pdf_document.create_page(0)
    renderer = PageRenderer()
    image = renderer.render_page(page_1)
    return image.data

def main():
    pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']
    pool = multiprocessing.Pool(processes=4)
    results = pool.map(process_pdf, pdf_files)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
