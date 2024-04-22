from pandas import read_csv, DataFrame
from .validators import DataFrameData
from .utils import error_loading

class CSVHandler:
    def load(file_path:str, encoding:str, mode:str = 'r'):
        try:
            return {'Unique': read_csv(file_path)}
        except Exception as error:
            return error_loading(file_path, error=error)

    def write(file_path:str, encoding:str, data:DataFrame|dict[str, DataFrame]):
        DataFrameData(data=data)
        if isinstance(data, DataFrame):
            data.to_csv(file_path, index=False)
            return
        if len(data.keys()) > 1:
            for k,v in data.items():
                v.to_csv(f'{file_path.replace(".csv", "")}_{k}.csv', index=False)
        else:
            list(data.values())[0].to_csv(file_path, index=False)
