from json import load, dump
from .validators import JsonData
from .utils import serialize_datetime, deserialize_datetime, error_loading

class JsonHandler:
    def load(file_path:str, encoding:str):
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = load(f)
            return {'Unique': deserialize_datetime(data)}
        except Exception as error:
            return error_loading(file_path, error=error)

    def write(file_path:str, encoding:str, data:dict[str, list|dict|str|int|float|bool|None]):
        JsonData(data=data)
        if len(data.keys()) == 1 and list(data.keys())[0] == 'Unique':
            data = list(data.values())[0]
        data = serialize_datetime(data)
        with open(file_path, 'w', encoding=encoding) as f:
            dump(data, f, indent=4)