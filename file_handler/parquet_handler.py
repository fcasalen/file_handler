from pandas import read_parquet, DataFrame
from .validators import DataFrameData
from .utils import error_loading

class ParquetHandler:
    @staticmethod
    def load(file_path_with_password:tuple[str, str], encoding:str, mode:str = 'r'):
        file_path, password = file_path_with_password
        try:
            return {'Unique': read_parquet(file_path)}
        except Exception as error:
            return error_loading(file_path, error=error)

    @staticmethod
    def write(file_path:str, encoding:str, data:DataFrame|dict[str, DataFrame], mode:str = 'w'):
        DataFrameData(data=data)
        if isinstance(data, DataFrame):
            data.to_parquet(file_path, index=False)
            return
        if len(data.keys()) > 1:
            for k,v in data.items():
                v.to_parquet(f'{file_path.replace(".parquet", "")}_{k}.parquet', index=False)
        else:
            list(data.values())[0].to_parquet(file_path, index=False)
