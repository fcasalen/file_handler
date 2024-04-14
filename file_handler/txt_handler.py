from .validators import TxtData
from .utils import error_loading

class TxtHandler:
    def load(file_path:str, encoding:str):
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = f.read()
            return {'Unique': data}
        except Exception as error:
            return error_loading(file_path, error=error)

    def write(file_path:str, encoding:str, data:dict[str, str]):
        TxtData(data=data)
        if len(data.keys()) > 1:
            data = [f'{k}\n{v}' for k,v in data.items()]
            data = "\n\n".join(data)
        else:
            data = list(data.values())[0]
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(data)