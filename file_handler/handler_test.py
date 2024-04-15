from os.path import dirname, join
from .handler import FileHandler
from .json_handler import JsonHandler

def test_all():
    file_path = join(dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    data = FileHandler.load(file_paths=file_path)
    data_expected = JsonHandler.load(file_path=join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), encoding='utf-8')['Unique']
    assert data == {file_path: data_expected}
    data = FileHandler.load(file_paths=join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), load_first_value=True)
    data_expected = JsonHandler.load(file_path=join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), encoding='utf-8')['Unique']
    assert data == data_expected