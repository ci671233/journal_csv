import os
import csv
from collections import namedtuple
from multiprocessing import Manager

class FileHandler:
    Result = namedtuple('Result', ['author', 'university', 'title', 'acknowledgement'])

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def get_pdf_files(self):
        # PDF 파일 목록을 반환합니다.
        return [file for file in os.listdir(self.input_path) if file.endswith('.pdf')]

    def write_to_csv(self, results_queue):
        # 결과를 CSV 파일로 저장합니다.
        with open(self.output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(FileHandler.Result._fields)
            while True:
                result = results_queue.get()
                if result is None:
                    break
                writer.writerow(result)

    def get_results_queue(self):
        # 병렬 처리를 위한 결과 큐를 반환합니다.
        manager = Manager()
        return manager.Queue()