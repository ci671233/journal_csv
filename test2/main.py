import os
from multiprocessing import Pool
from test.FileHandler import FileHandler
from test.PdfReader import PdfReader
from test.OpenaiInferencer import OpenaiInferencer

def process_file(file_path, results_queue):
    pdf_reader = PdfReader(file_path)
    text = pdf_reader.get_text()

    openai_inferencer = OpenaiInferencer(openai_key)
    result = openai_inferencer.infer(text)

    results_queue.put(result)

def main():
    input_path = "./input"
    output_path = "./output/results.csv"  # Here, specify the output CSV file.
    openai_key = "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"
    file_handler = FileHandler(input_path, output_path)
    
    results_queue = file_handler.get_results_queue()
    with Pool() as pool:
        files = [os.path.join(input_path, pdf_file) for pdf_file in file_handler.get_pdf_files()]
        for file_path in files:
            pool.apply_async(process_file, (file_path, results_queue))

    file_handler.write_to_csv(results_queue)

if __name__ == "__main__":
    main()