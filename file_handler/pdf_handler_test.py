from os.path import dirname, join
from .pdf_handler import PDFHandler
from .json_handler import JsonHandler

def test_all():
    this_dir = dirname(__file__)
    pdf_data = PDFHandler.load(file_path_with_password=(join(this_dir, 'mocks/somatosensory.pdf'), None), encoding='utf-8')
    assert pdf_data == JsonHandler.load(file_path_with_password=(join(this_dir, 'mocks/somatosensory_extracted.json'), None), encoding='utf-8')['Unique']