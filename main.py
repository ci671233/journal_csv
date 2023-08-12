from journal import Journal
from journal_manage import JournalManagement
from config import *
import logging

logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
