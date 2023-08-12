import glob
import pandas as pd
from journal import Journal
from config import *
import openai

class JournalManagement:
    def __init__(self, ai_key, model, path, output_path):
        openai.api_key = ai_key
        self.model = model
        self.path = path
        self.output_path = output_path
        self.result_data = []
        self.pdf_list = []

    def process_pdfs(self):
        self.pdf_list = glob.glob(os.path.join(self.path, "*.pdf"))
        print(f"Found {len(self.pdf_list)} PDFs.")
        for pdf_path in self.pdf_list:
            print(f"Processing {pdf_path}...")
            journal = Journal(pdf_path)
            result = journal.process_journal()
            if result == "image파일입니다":
                self.result_data.append({
                    "title": "Image-based PDF", 
                    "author": "Image-based PDF", 
                    "acknowledgements": "Image-based PDF"
                })
            else:
                front_data, acknowledgements = result
                chat_response = self.ask_ai(front_data)
                self.result_data.append({
                    "title": chat_response["title"], 
                    "author": chat_response["authors"], 
                    "acknowledgements": acknowledgements
                })
            print(f"Done processing {pdf_path}.")
        
        print("Converting data to CSV...")
        self.data_to_csv()
        print("Done converting data to CSV.")

    def ask_ai(self, data):
        print("Asking AI for title and authors...")
        prompt = f"다음 텍스트는 연구 논문의 처음 몇 페이지에서 가져온 것입니다:\n\n{data}\n\ntitle : \nauthors : \n지금 너에게 준 형식들로 맞춰서 나에게 알려줘(형식을 절대 바꾸지 말고 꼭 유지해줘)\n 항목이 여러개인 경우 ','으로 구분해주고 항목이 없을 경우 None으로 표시해줘\n"
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        lines = response.choices[0].message.content.strip().split("\n")
        
        result = {}
        for line in lines:
            if line.lower().startswith("title:"):
                result["title"] = line.split(":")[1].strip()
            elif line.lower().startswith("authors:"):
                result["authors"] = line.split(":")[1].strip()
                
        # If AI did not return title or authors, set default values.
        if "title" not in result:
            result["title"] = "Unknown Title"
        if "authors" not in result:
            result["authors"] = "Unknown Authors"

        print("Received response from AI.\n") 
        return result


    def data_to_csv(self):
        df = pd.DataFrame(self.result_data)
        df.to_csv(os.path.join(self.output_path, "output.csv"), index=False)