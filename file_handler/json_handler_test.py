from os.path import dirname, join
from os import remove
from datetime import datetime
from .json_handler import JsonHandler

def test_all():
    data = {'ha': ['ha']}
    file_path = join(dirname(__file__), 'txt_handler_test.json')
    JsonHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert JsonHandler.load(file_path=file_path, encoding='utf-8') == {'Unique': data}
    data = {'Unique': ['ha']}
    file_path = join(dirname(__file__), 'txt_handler_test.json')
    JsonHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert JsonHandler.load(file_path=file_path, encoding='utf-8') == {'Unique': list(data.values())[0]}
    fake_dt = datetime(2023,1,1)
    data = {
        'ha': [fake_dt],
        "lol": ["lol"]
    }
    JsonHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert JsonHandler.load(file_path=file_path, encoding='utf-8') == {
        'Unique': {
            'ha': [fake_dt.isoformat()],
            'lol': ['lol']
        }
    }
    data = {
        'one': {
            'ha': fake_dt,
            "lol": "lol"
        },
        'two': ['lol2']
    }
    JsonHandler.write(file_path=file_path, encoding='utf-8', data=data)
    assert JsonHandler.load(file_path=file_path, encoding='utf-8') == {
        'Unique': {
            'one': {
                'ha': fake_dt.isoformat(),
                'lol': 'lol'
            },
            'two': ['lol2']
        }
    }
    remove(file_path)
    