from .handler import FileHandler, decider
from .json_handler import JsonHandler
import os
import re

def test_pptx_single_and_multi_process():
    file_path = os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    data = FileHandler.load(file_paths=file_path)
    data_expected = JsonHandler.load(
        file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == {file_path: data_expected}
    data = FileHandler.load(file_paths=file_path, multiprocess=True)
    assert data == {file_path: data_expected}
    data = FileHandler.load(file_paths=os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == data_expected

def test_json_and_ppt_writing_at_same_time():
    file_path = os.path.join(os.path.dirname(__file__), 'mocks/test.json')
    json_data = {'test_key': 2}
    FileHandler.write(file_handler_data={file_path: json_data})
    data = FileHandler.load(file_paths=file_path)
    assert data == {file_path: {'Unique': json_data}}
    file_path2 = os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    FileHandler.write(file_handler_data={file_path: json_data} | FileHandler.load(file_paths=file_path2), multiprocess=True)
    data = FileHandler.load(file_paths=[file_path, file_path2], multiprocess=True)
    assert data == {
        file_path: {'Unique': json_data},
        file_path2: JsonHandler.load(
            file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
            encoding='utf-8'
        )['Unique']
    }
    os.remove(file_path)
    data = FileHandler.load(file_paths=os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == data_expected

def test_pdf_and_pptx_at_same_time():
    file_path = os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    file_path2 = os.path.join(os.path.dirname(__file__), 'mocks/somatosensory.pdf')
    data = FileHandler.load(file_paths=[file_path, file_path2], multiprocess=True, load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']['Slide 1']
    data_expected2 = JsonHandler.load(
        file_path_with_password=(os.path.join(os.path.dirname(__file__), 'mocks/somatosensory_extracted.json'), None),
        encoding='utf-8'
    )['Unique']['Page 1']
    assert data == {file_path: data_expected, file_path2: data_expected2}

def test_txt():
    file_path = os.path.join(os.path.dirname(__file__), 'mocks/test.txt')
    json_data = 'oi'
    FileHandler.write(file_handler_data={file_path: json_data})
    data = FileHandler.load(file_paths=file_path)
    assert data == {file_path: {'Unique': json_data}}
    os.remove(file_path)

def test_json_with_list():
    file_path = os.path.join(os.path.dirname(__file__), 'mocks/test.json')
    FileHandler.write(file_handler_data={file_path: [1, 2]})
    data = FileHandler.load(file_paths=file_path)
    assert data == {file_path: {'Unique': [1, 2]}}
    os.remove(file_path)
    
def test_decider_uses_all_handlers():
    handlers = []
    dir = os.path.dirname(__file__)
    for file in os.listdir(dir):
        if '_test' in file or not file.endswith('.py') or '_handler' not in file:
            continue
        with open(os.path.join(dir, file), 'r') as f:
            code = f.read()
        handlers.extend(re.findall('class (.*?):', code))

    assert set([f.__name__ for f in decider.values()]) == set(handlers)

    