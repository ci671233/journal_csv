from journal import Journal
from journal_manage import JournalMangaement
from config import *

ai_key = OPENAI_KEY
path = INPUT_PATH
output_path = OUTPUT_PATH
model = "gpt-3.5-turbo"
jour_manage = JournalMangaement(ai_key, model, path, output_path)

jour_manage.set_journal_list()
jour_manage.run_ai()
jour_manage.data_to_csv()

# 추후 수정 필요한 사항
# data_clensing_front 함수 수정