import fitz
import pytesseract
import os
from PIL import Image

class Journal: 
    def __init__(self, path):
        self.path = path
        self.doc = fitz.open(self.path)
        self.image_pages = []
        self.text_pages = []
        self.acknowledgements = "none"

    def process_journal(self):
        print("Processing journal...")
        for i in range(len(self.doc)):
            page = self.doc.load_page(i)
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            if pytesseract.image_to_string(image):
                self.text_pages.append(i)
            else:
                self.image_pages.append(i)
        
        if not self.text_pages:
            print("Journal is an image-based PDF.")
            return "image파일입니다"
        
        self.front_data = self.process_text_pages()

        self.search_acknowledgements()
        
        print("Done processing journal.")
        return self.front_data, self.acknowledgements

    def process_text_pages(self):
        # Only use the first two pages to avoid exceeding token limit
        pages_to_process = min(2, len(self.text_pages))
        pages = self.text_pages[:pages_to_process]
        
        data = ""
        for page_num in pages:
            page = self.doc.load_page(page_num)
            text = page.get_text()
            data += text

        return data

    def search_acknowledgements(self):
        print("Searching for acknowledgements...")
        keywords = ["acknowl", "감사의", "funding", "contributions", "지원을받아"]
        found = False

        for page_num in reversed(self.text_pages):
            page = self.doc.load_page(page_num)
            text = page.get_text().lower().replace(" ", "")

            for keyword in keywords:
                keyword_index = text.find(keyword)
                
                if keyword_index != -1:
                    self.acknowledgements = "acknowledgements : exist"
                    found = True
                    break

            if found:
                break

        if not found:
            print("No acknowledgements found.")
            self.acknowledgements = "acknowledgements : none"
        else:
            print("Acknowledgements found.")
    
    # def data_clensing_back(self):
    #     bac_data = "" 
    #     keywords = ["acknowl", "감사의", "funding", "contributions"]
    #     found = False  

    #     for i in reversed(range(len(self.back))):  
    #         page = self.back[i]  
    #         check = page.lower().replace(" ", "")  
    #         print(check)
    #         for keyword in keywords:  
    #             keyword_index = check.find(keyword)  

    #             if keyword_index != -1:  
    #                 start_index = keyword_index  
    #                 end_index = min(len(check), keyword_index + 275)  # Keyword + next 300 characters
    #                 bac_data = "\nacknowledgements : " + check[start_index + len(keyword):end_index]  
    #                 print("\nfound!\n")
    #                 print(bac_data)
    #                 self.data += bac_data  
    #                 found = True  
    #                 break  

    #         if found:  
    #             break

    #     if not found:  
    #         self.data += "acknowledgements 없음, 감사의 문구 없음"
