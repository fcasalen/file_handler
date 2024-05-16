from os.path import dirname, join
from .ppt_handler import PPTHandler
from .json_handler import JsonHandler

def test_all():
    this_dir = dirname(__file__)
    slide_data = PPTHandler.load(
        file_path_with_password=(join(this_dir, 'mocks/Dickinson_Sample_Slides.pptx'), None),
        encoding='utf-8'
    )
    assert slide_data == JsonHandler.load(
        file_path_with_password=(join(this_dir, 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']