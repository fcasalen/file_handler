from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure#, LTImage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFPasswordIncorrect
from warnings import warn
# import pytesseract
# from PIL import Image
#from io import BytesIO
from .validators import TxtData
from .utils import error_loading, adjust_phrases

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\xxxx\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe'

class PDFHandler:
    @staticmethod
    def load(file_path_with_password:tuple[str, str], encoding:str, mode:str = 'r'):
        file_path, password = file_path_with_password
        try:
            with open(file_path, 'rb') as file:
                parser = PDFParser(file)
                PDFDocument(parser, password=password)
        except PDFPasswordIncorrect:
            warn_msg = f"PDF file {file_path} is encrtyped. Need password! Loading data with this error meessage!"
            warn(warn_msg)
            return {'Unique': warn_msg}
        try:
            pages = {}
            for numPage, pagina_layout in enumerate(extract_pages(pdf_file=file_path, password=password), start=1):
                page_text = ""
                for element in pagina_layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        page_text += element.get_text()
                    elif isinstance(element, LTFigure):
                        pass
                        # page_text += extract_text_from_image(element=element, numPage=numPage)
                pages[f'Page {numPage}'] = adjust_phrases(page_text)
            return pages
        except Exception as error:
            return error_loading(file_path, error=error)

    @staticmethod
    def write(file_path:str, encoding:str, data:dict[str, str], mode:str = 'w'):
        TxtData(data=data)
        print("I can't write pdf files yet!")


# def extract_text_from_image(element:LTFigure, numPage:int):
#     text = ''
#     for subel in element:
#         if not isinstance(subel, LTImage):
#             continue
#         try:
#             imagem_bytes = subel.stream.get_rawdata()
#             image = Image.open(BytesIO(imagem_bytes))
#             text += pytesseract.image_to_string(image)
#         except Exception:
#             print(f"Couldn't get text from image in page {numPage}")
#     return text


