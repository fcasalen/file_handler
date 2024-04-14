from os.path import dirname, join
from os import remove
from .txt_handler import TxtHandler

def test_all():
    data = {'ha': 'ha'}
    file_path = join(dirname(__file__), 'txt_handler_test.txt')
    TxtHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert TxtHandler.load(file_path=file_path, encoding='utf-8') == {'Unique': list(data.values())[0]}
    data = {
        'ha': 'ha',
        "lol": "lol"
    }
    TxtHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert TxtHandler.load(file_path=file_path, encoding='utf-8') == {'Unique': 'ha\nha\n\nlol\nlol'}
    remove(file_path)
    