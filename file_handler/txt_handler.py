from .validators import TxtData
from .utils import error_loading

class TxtHandler:
    @staticmethod
    def load(file_path_with_password:tuple[str, str], encoding:str, mode:str = 'r'):
        file_path, password = file_path_with_password
        try:
            if mode == 'rb':
                encoding = None
            with open(file_path, mode=mode, encoding=encoding) as f:
                data = f.read()
            return {'Unique': data}
        except Exception as error:
            return error_loading(file_path, error=error)

    @staticmethod
    def write(file_path:str, encoding:str, data:bytes|str|dict[str, str], mode:str = 'w'):
        TxtData(data=data)
        if isinstance(data, bytes):
            print('will write in wb mode, since the input is bytes')
            mode = 'wb'
        if mode == 'wb':
            encoding = None
        if not isinstance(data, str):
            if len(data.keys()) == 1 and list(data.keys())[0] == 'Unique':
                data = list(data.values())[0]
            else:
                data = [f'{k}\n{v}' for k,v in data.items()]
                data = "\n\n".join(data)
        with open(file_path, mode=mode, encoding=encoding) as f:
            f.write(data)