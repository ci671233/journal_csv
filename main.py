from journal import Journal
from journal_manage import JournalManagement
from config import *

ai_key = OPENAI_KEY
path = INPUT_PATH
output_path = OUTPUT_PATH
model = "gpt-3.5-turbo"
jour_manage = JournalManagement(ai_key, model, path, output_path)

print("Starting to process PDFs...")
jour_manage.process_pdfs()
print("Done processing PDFs.")

print("Writing data to CSV...")
jour_manage.data_to_csv()
print("Done writing data to CSV.")

# 추후 수정 필요한 사항
# data_clensing_front 함수 수정