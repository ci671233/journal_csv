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
        self.acknowl = "" #journal acknolegement 
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
            return (1, 1, "abstract")
        elif page <= 10 :
            return (3, 2, "journal")
        else:
            return (3, 5, "journal")
    
    def check_data_type(self) :
        #Pdf : img or text
        for text in self.front : 
            self.data += text
            
        if len(self.data) <= 1000 :
            self.data_type = "image"
            
                
    def data_clensing_front(self) :      
        text = self.data.lower().replace(" ", "")
        #대소문자 구분 및 공백 제거
                
        #앞에 사사문구가 있을경우
        if "acknowledgment" in text or "감사의말" in text or "감사의글" in text:
            print("\n\n\n\nst_check")
            return False           
        print("\n\n\n\ntest_check")
        self.data = self.data[:1300]
        return True
    
    def data_clensing_back(self) : 
        bac_data = ""
        #keyword = "참고"
        keywords = ["참고", "reference"]
        for page in reversed(self.back) :
            check = page.lower().replace(" ", "")
            #사사문구 페이지
            if "acknowl" in check or "감사의말" in check or "감사의글" in check :
                # bac_data = page.lower().replace(" ", "")
                for keyword in keywords:
                    keyword_index = check.find(keyword)
                    start_index = max(0, keyword_index - 200)
                    bac_data = check[start_index:keyword_index] 
                    print(bac_data)
                    self.data += bac_data
                    break 
             
            
            # #참고 논문과 이전페이지만 봄        
            # if "reference" in check or "참고" in check :
            #     bac_data = page
            #     print("\n\n\n\test_check")
            #     continue
            
        
        self.data += check
    
    def get_data(self) :
        
        return self.data