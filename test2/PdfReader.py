import fitz

class PdfReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_text(self):
        # PDF 파일에서 텍스트를 추출합니다.
        doc = fitz.open(self.file_path)
        text = ""
        for i, page in enumerate(doc):
            if len(doc) == 1 or len(doc) <= 3 and i in [0, -1] or len(doc) <= 10 and i in range(3) + range(-3, 0) or i in range(3) + range(-5, 0):
                text += page.get_text()
        return text