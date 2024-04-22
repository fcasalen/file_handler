from pandas import read_excel, DataFrame, ExcelWriter
from .validators import DataFrameData
from .utils import error_loading

class ExcelHandler:
    def load(file_path:str, encoding:str, mode:str = 'r'):
        try:
            return read_excel(file_path, sheet_name=None)
        except Exception as error:
            return error_loading(file_path, error=error)

    def write(file_path:str, encoding:str, data:DataFrame|dict[str, DataFrame], mode:str = 'w'):
        DataFrameData(data=data)
        if isinstance(data, DataFrame):
            data.to_excel(file_path, index=False)
            return
        with ExcelWriter(file_path) as writer:
            for sheetname, df in data.items():
                df.to_excel(writer, sheet_name=sheetname, index=False)