from os.path import dirname, join
from os import remove
from .handler import FileHandler
from .json_handler import JsonHandler

def test_all():
    file_path = join(dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    data = FileHandler.load(file_paths=file_path)
    data_expected = JsonHandler.load(
        file_path_with_password=(join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == {file_path: data_expected}
    data = FileHandler.load(file_paths=file_path, multiprocess=True)
    assert data == {file_path: data_expected}
    data = FileHandler.load(file_paths=join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == data_expected
    file_path = join(dirname(__file__), 'mocks/test.json')
    json_data = {'test_key': 2}
    FileHandler.write(file_handler_data={file_path: json_data})
    data = FileHandler.load(file_paths=file_path)
    assert data == {file_path: {'Unique': json_data}}
    file_path2 = join(dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    FileHandler.write(file_handler_data={file_path: json_data} | FileHandler.load(file_paths=file_path2), multiprocess=True)
    data = FileHandler.load(file_paths=[file_path, file_path2], multiprocess=True)
    assert data == {
        file_path: {'Unique': json_data},
        file_path2: JsonHandler.load(
            file_path_with_password=(join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
            encoding='utf-8'
        )['Unique']
    }
    remove(file_path)
    data = FileHandler.load(file_paths=join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']
    assert data == data_expected
    file_path = join(dirname(__file__), 'mocks/Dickinson_Sample_Slides.pptx')
    file_path2 = join(dirname(__file__), 'mocks/somatosensory.pdf')
    data = FileHandler.load(file_paths=[file_path, file_path2], multiprocess=True, load_first_value=True)
    data_expected = JsonHandler.load(
        file_path_with_password=(join(dirname(__file__), 'mocks/Dickinson_Sample_Slides_extracted.json'), None),
        encoding='utf-8'
    )['Unique']['Slide 1']
    data_expected2 = JsonHandler.load(
        file_path_with_password=(join(dirname(__file__), 'mocks/somatosensory_extracted.json'), None),
        encoding='utf-8'
    )['Unique']['Page 1']
    assert data == {file_path: data_expected, file_path2: data_expected2}
    file_path = join(dirname(__file__), 'mocks/test.txt')
    json_data = 'oi'
    FileHandler.write(file_handler_data={file_path: json_data})
    data = FileHandler.load(file_paths=file_path)
    assert data == {file_path: {'Unique': json_data}}
    remove(file_path)