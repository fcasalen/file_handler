from json import load, dump
from .validators import JsonData
from .utils import serialize_datetime, error_loading

class JsonHandler:
    @staticmethod
    def load(file_path_with_password:tuple[str, str], encoding:str, mode:str = 'r'):
        file_path, password = file_path_with_password
        try:
            if mode == 'rb':
                encoding = None
            with open(file_path, mode=mode, encoding=encoding) as f:
                data = load(f)
            return {'Unique': data}
        except Exception as error:
            return error_loading(file_path, error=error)

    @staticmethod
    def write(file_path:str, encoding:str, data:list|dict[str, list|dict|str|int|float|bool|None], mode:str = 'w'):
        JsonData(data=data)
        if isinstance(data, bytes):
            print('will write in wb mode, since the input is bytes')
            mode = 'wb'
        if mode == 'wb':
            encoding = None
        if isinstance(data, dict):
            if len(data.keys()) == 1 and list(data.keys())[0] == 'Unique':
                data = list(data.values())[0]
        data = serialize_datetime(data)
        with open(file_path, mode=mode, encoding=encoding) as f:
            dump(data, f, indent=4)