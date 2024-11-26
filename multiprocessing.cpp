#include <iostream>
#include <cstdlib>
#include <chrono>

void process_page_with_easyocr(int page_num, const std::string &image_path) {
    try {
        std::string command = "ec_ocr.py " + image_path;
        int result = system(command.c_str());
        if (result != 0) {
            std::cerr << "Error executing Python script for page " << page_num << std::endl;
        }
    } catch (const std::exception &e) {
        std::cerr << "Error during OCR processing: " << e.what() << std::endl;
    }
}

void convert_pdf_to_image(const std::string &pdf_path, int first_page, int last_page) {
    for (int page_num = first_page; page_num <= last_page; ++page_num) {
        std::string image_path = "processed_page_" + std::to_string(page_num) + ".png";
        process_page_with_easyocr(page_num, image_path);
    }
}

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::string pdf_path = "OCR_extraction.pdf";
    int first_page = 1;
    int last_page = 4;
    convert_pdf_to_image(pdf_path, first_page, last_page);
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> total_duration = end_time - start_time;
    std::cout << "Total time for processing: " << total_duration.count() << " seconds." << std::endl;
    return 0;
}