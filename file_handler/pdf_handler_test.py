from os.path import dirname, join
from .pdf_handler import PDFHandler
from .json_handler import JsonHandler

def test_all():
    this_dir = dirname(__file__)
    pdf_data = PDFHandler.load(file_path=join(this_dir, 'mocks/somatosensory.pdf'), encoding='utf-8')
    assert pdf_data == JsonHandler.load(file_path=join(this_dir, 'mocks/somatosensory_extracted.json'), encoding='utf-8')['Unique']