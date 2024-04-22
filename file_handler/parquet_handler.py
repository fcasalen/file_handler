from pandas import read_parquet, DataFrame
from .validators import DataFrameData
from .utils import error_loading

class ParquetHandler:
    def load(file_path:str, encoding:str, mode:str):
        try:
            return {'Unique': read_parquet(file_path)}
        except Exception as error:
            return error_loading(file_path, error=error)

    def write(file_path:str, encoding:str, data:dict[str, DataFrame]):
        DataFrameData(data=data)
        if len(data.keys()) > 1:
            for k,v in data.items():
                v.to_parquet(f'{file_path.replace(".parquet", "")}_{k}.parquet', index=False)
        else:
            list(data.values())[0].to_parquet(file_path, index=False)
