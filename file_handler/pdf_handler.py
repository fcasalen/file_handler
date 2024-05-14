from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure, LTImage
# import pytesseract
# from PIL import Image
from tqdm import tqdm
from io import BytesIO
from .validators import TxtData
from .utils import error_loading, adjust_phrases

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\xxxx\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe'

class PDFHandler:
    def load(file_path:str, encoding:str, mode:str = 'r'):
        try:
            pages = {}
            for numPage, pagina_layout in tqdm(enumerate(extract_pages(file_path), start=1), desc = f'Extracting pages from pdf file {file_path}'):
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


