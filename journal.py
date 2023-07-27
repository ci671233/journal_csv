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
            return (1, 1, "abstract")
        elif page <= 10 :
            return (2, 2, "journal")
        else:
            return (2, 4, "journal")
    
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
        if "acknowl" in text or "감사의" in text :
            print("\nst_check")
            return False           
        print("\ntest_check")
        self.data = self.data[:1300]
        return True
    
    def data_clensing_back(self):
        bac_data = "" # Create an empty string bac_data
        keywords = ["참고", "reference"] # Define the list of keywords to search for
        found = False  # A flag variable to check if the keywords are found

        for i in reversed(range(len(self.back))):  # Iterate through each page index from back to front
            page = self.back[i]  # Get the page text
            check = page.lower().replace(" ", "")  # Convert the page text to lower case and remove all spaces

            # If either "참고" or "reference" is found in the text
            if any(keyword in check for keyword in keywords): 
                # Combine the current and previous page into a single string
                if i > 0:  # Check if there is a previous page
                    prev_page = self.back[i - 1]
                    combined_text = prev_page + page
                else:
                    combined_text = page

                # Convert the combined text to lower case and remove all spaces
                combined_text = combined_text.lower().replace(" ", "")

                # If either "acknowl" or "감사의" is found in the combined text
                if "acknowl" in combined_text or "감사의" in combined_text:
                    for keyword in keywords:  # Iterate through each keyword
                        keyword_index = combined_text.find(keyword)  # Find the index of the keyword in the text

                        if keyword_index != -1:  # If keyword is found
                            start_index = max(0, keyword_index - 200)  # Calculate the start index for slicing the string
                            bac_data = combined_text[start_index:keyword_index]  # Slice the string from start_index to keyword_index
                            self.data += bac_data  # Append the sliced string to self.data
                            found = True  # Set the found flag to True
                            break  # Break the loop
                else:  # If neither "acknowl" nor "감사의" is found in the combined text
                    self.data += "acknowledgements 없음"  # Append "acknowledgements 없음" to self.data
                    found = True  # Set the found flag to True

            if found:  # If the keyword was found, break the loop
                break

        if not found:  # If the loop finishes without finding the keywords, append "acknowledgements 없음" to self.data
            self.data += "acknowledgements 없음"
    
    def get_data(self) :
        
        return self.data