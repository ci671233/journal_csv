import openai
import glob
from journal import Journal
import pandas as pd
import time

class JournalMangaement :
    def __init__(self, ai_key, model, path, output_path):
        openai.api_key = ai_key
        self.model = model
        self.path = path
        self.pdf_list = []
        self.result_data = []
        self.key = ["title", "title-kor", "author", "author's-affiliation", "acknowledgements"]
        self.first_q = "title : \ntitle-kor : \n\
            author : \nauthor's-affiliation : \n\
            acknowledgements : \n"
        # self.key = ["title-eng", "title-kor", "author-eng", "author-kor", "acknowledgments"]
        # self.first_q = "title-English : \ntitle-Korean : \n\
        #     author-English : \nauthor-Korean : \n\
        #     acknowledgments : \n"
        self.output_path = output_path
        self.sleep_interval = 1
        
    def set_journal_list(self) :    #주어진 경로에서 모든 PDF 파일의 경로를 찾아서 pdf_list에 저장
        self.pdf_list = glob.glob(f'{self.path}/*.pdf')
        print(f"Found {len(self.pdf_list)} PDF files")  # 파일 개수 출력
        
    def get_journal(self) :
        if self.pdf_list == [] :
            return None
        return self.pdf_list.pop()
    
    def set_ai_content(self, path) :
        journal = Journal(path)
        journal.read_text()
        journal.check_data_type()
        if journal.data_type == "image":
            return {"title": "Image-based PDF", "title-kor" : "Image-based PDF", "author": "Image-based PDF", "author's-affiliation": "Image-based PDF", "acknowledgments": "Image-based PDF"}   
        if journal.data_clensing_front() :
            journal.data_clensing_back()
        return f"해당 논문에서 {self.first_q} \n지금 너에게 준 형식들로 맞춰서 나에게 알려줘\n 없을 경우 None으로 표시해줘\n" + journal.get_data() 
        
    def input_text(self, data) :
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": data}, 
                    ]
                )
                print(response.choices[0].message.content)  # AI 응답 출력
                self.sleep_interval = max(1, self.sleep_interval - 0.1)  # 요청 성공시 대기 시간 10% 감소, 최소 1초
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error in OpenAI request: {e}")
                self.sleep_interval *= 2  # 요청 실패시 대기 시간 2배 증가
                print(f"Waiting for {self.sleep_interval} seconds before retrying.")
                time.sleep(self.sleep_interval)
    
    def result_to_dictionary(self, result) : 
        lines = result.split("\n")
        data = {}
        for line in lines:
            for key in self.key:
                if line.lower().startswith(key):
                    _, value = line.split(": ", 1)
                    data[key] = value
                    break
        self.result_data.append(data)
        print(data)


    
    def run_ai(self) : 
        total_files = len(self.pdf_list)  # 총 파일 수 저장
        for i, path in enumerate(self.pdf_list, start=1): 
            try:
                print(f"Processing file {i} of {total_files}: {path}")  # 현재 처리 중인 파일 정보 출력
                content = self.set_ai_content(path)
                if isinstance(content, dict):
                    self.result_data.append(content)
                    continue
                result = self.input_text(content)
                time.sleep(1)
                self.result_to_dictionary(result)
            except Exception as e:
                print(f"Error processing file {path}: {e}")
            
            
    def data_to_csv(self) :
        df = pd.DataFrame.from_records(self.result_data)
        df.to_csv(f"{self.output_path}/output.csv", index=False)