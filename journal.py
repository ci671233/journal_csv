import fitz
import pytesseract
import os
from PIL import Image
import logging

logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class Journal: 
    def __init__(self, path):
        self.path = path
        self.doc = fitz.open(self.path)
        self.image_pages = []
        self.text_pages = []
        self.acknowledgements = "none"

    def process_journal(self):
    print("논문을 처리 중입니다...")

        # 전체 페이지를 순회하면서
        for i in range(len(self.doc)):
            page = self.doc.load_page(i)  # i번째 페이지 로드
            pix = page.get_pixmap()  # 페이지를 이미지(pixmap)로 변환
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # PIL 이미지 객체로 변환
            logging.info(f"파일 처리 중: {self.path}, 페이지: {i}")  # 로그 기록
    
            # OCR(문자인식)을 통해 텍스트 존재 여부 확인
            if pytesseract.image_to_string(image):
                self.text_pages.append(i)  # 텍스트가 있는 페이지로 분류
            else:
                self.image_pages.append(i)  # 텍스트가 없는, 이미지 기반 페이지로 분류
    
        # 텍스트가 하나도 없으면 이미지 기반 PDF로 판단
        if not self.text_pages:
            print("이 논문은 이미지 기반 PDF입니다.")
            return "image파일입니다"
    
        # 텍스트가 있는 경우, 전처리 수행
        self.front_data = self.process_text_pages()
    
        # 감사 인사(Acknowledgements) 문단 탐색
        self.search_acknowledgements()
        
        print("논문 처리 완료.")
        return self.front_data, self.acknowledgements



    def process_text_pages(self):
        # OpenAI 토큰 제한 때문에 한 번에 최대 2페이지까지만 처리
        pages_to_process = min(2, len(self.text_pages))  # 텍스트 페이지 수가 2개보다 적으면 그 수만큼
        pages = self.text_pages[:pages_to_process]  # 앞쪽에서 최대 2페이지 추출
    
        data = ""  # 텍스트 누적용 변수
        for page_num in pages:
            page = self.doc.load_page(page_num)  # 해당 페이지 로드
            text = page.get_text()  # 페이지에서 텍스트 추출
            data += text  # 전체 데이터에 이어붙이기
            logging.info(f"Page {page_num}: {text}")  # 로그로 해당 페이지 텍스트 출력
    
        return data  # 텍스트 전체 반환



    def search_acknowledgements(self):
        print("감사의 글(Acknowledgements) 탐색 중...")
        
        # 키워드 목록 (영문/한글 혼용)
        keywords = ["acknowl", "감사의", "funding", "contributions", 
                    "supportedby", "지원을받아", "지원과제"]
    
        found = False  # 찾았는지 여부 플래그
    
        # 텍스트 페이지들을 뒤에서부터 확인 (보통 뒤쪽에 acknowledgements가 있음)
        for page_num in reversed(self.text_pages):
            page = self.doc.load_page(page_num)  # 페이지 로드
            text = page.get_text().lower().replace(" ", "")  # 텍스트 추출 후, 모두 소문자+공백 제거
    
            # 키워드 중 하나라도 포함되어 있으면 감지
            for keyword in keywords:
                keyword_index = text.find(keyword)
                
                if keyword_index != -1:
                    self.acknowledgements = "acknowledgements : exist"  # 존재함 표시
                    found = True
                    break  # 키워드 찾았으니 더 이상 볼 필요 없음
    
            if found:
                break  # 찾았으면 페이지 반복도 종료
    
        # 최종 결과 출력
        if not found:
            print("감사의 글이 발견되지 않았습니다.")
            self.acknowledgements = "acknowledgements : none"
        else:
            print("감사의 글이 존재합니다.")

