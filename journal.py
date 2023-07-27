import fitz
from pdf2image import convert_from_path
from pytesseract import *
from PIL import Image

class Journal : 
    def __init__(self, path) :
        self.type = "text" #journal or abstract
        self.data_type = "" #text or img
        
        self.data = "" #journal text
        
        self.path = path #pdf path
        
        self.title = "" #journal title
        self.acknowlgements = "" #journal acknolegements
        self.author = [] #journal Author
        
        
        #front : fitz document
        #back : fitz document
            
    def read_text(self) : 
        #journal의 type 설정 후 확인 데이터 확인
        doc = fitz.open(self.path)
        front, back, self.type = self.count(len(doc))
        
        text = []
        for page in doc :
            page = page.get_text()
            text.append(page)
        self.front = text[:front]
        self.back = text[-back:]
        
    def count(self, page) : 
        #1페이지, 2~3페이지, 10페이지 이하, 30페이지 이하, 이상
        if page <= 1 :
            return (1, 0, "abstract")
        elif page <= 3 :
            return (1, 2, "abstract")
        elif page <= 10 :
            return (3, 5, "journal")
        else:
            return (3, 8, "journal")
    
    def check_data_type(self) :
        #Pdf : img or text
        for text in self.front : 
            self.data += text
            
        if len(self.data) <= 1000 :
            self.data_type = "image"
            
                
    def data_clensing_front(self) :      
        #추후에 수정해야됨!
        text = self.data.lower().replace(" ", "")
        #대소문자 구분 및 공백 제거
                
        #앞에 사사문구가 있을경우
        if "acknowl" in text or "감사의" in text :
            print("\nst_check")
            return False           
        print("\ntest_check")
        self.data = self.data[:1300]
        return True
    
    def data_clensing_back(self):
        bac_data = "" 
        keywords = ["acknowl", "감사의", "funding", "contributions"]
        found = False  

        for i in reversed(range(len(self.back))):  
            page = self.back[i]  
            check = page.lower().replace(" ", "")  
            print(check)
            for keyword in keywords:  
                keyword_index = check.find(keyword)  

                if keyword_index != -1:  
                    start_index = keyword_index  
                    end_index = min(len(check), keyword_index + 275)  # Keyword + next 300 characters
                    bac_data = "\nacknowledgements : " + check[start_index + len(keyword):end_index]  
                    print("\nfound!\n")
                    print(bac_data)
                    self.data += bac_data  
                    found = True  
                    break  

            if found:  
                break

        if not found:  
            self.data += "acknowledgements 없음, 감사의 문구 없음"
    
    # def data_clensing_back(self):
    #     bac_data = "" 
    #     keywords = ["참고", "reference"] 
    #     found = False  # A flag variable to check if the keywords are found

    #     for i in reversed(range(len(self.back))):  # Iterate through each page index from back to front
    #         page = self.back[i]  # Get the page text
    #         check = page.lower().replace(" ", "")  # Convert the page text to lower case and remove all spaces

            
    #         if any(keyword in check for keyword in keywords): 
    #             if i > 0:  
    #                 prev_page = self.back[i - 1]
    #                 combined_text = prev_page + page
    #             else:
    #                 combined_text = page

    #             combined_text = combined_text.lower().replace(" ", "")

    #             if "acknowl" in combined_text or "감사의" in combined_text or "contributions" in combined_text or "funding" in combined_text:
    #                 for keyword in keywords:  
    #                     keyword_index = combined_text.find(keyword)  

    #                     if keyword_index != -1:  
    #                         start_index = max(0, keyword_index - 800)  
    #                         bac_data = combined_text[start_index:keyword_index]  
    #                         self.data += bac_data  
    #                         found = True  
    #                         break  
    #             else:  
    #                 self.data += "acknowledgements 없음, 감사의 문구 없음"  
    #                 found = True 

    #         if found:  
    #             break

    #     if not found:  
    #         self.data += "acknowledgements 없음, 감사의 문구 없음"
    
    def get_data(self) :
        
        return self.data