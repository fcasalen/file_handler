from pandas import read_excel, DataFrame, ExcelWriter, NA
from .validators import DataFrameData
from .utils import error_loading

class ExcelHandler:
    @staticmethod
    def load(file_path_with_password:tuple[str, str], encoding:str, mode:str = 'r'):
        file_path, password = file_path_with_password
        try:
            df_dict = read_excel(file_path, sheet_name=None)
            for sht in df_dict:
                df_dict[sht] = df_dict[sht].fillna(NA)
            return df_dict
        except Exception as error:
            return error_loading(file_path, error=error)

    @staticmethod
    def write(file_path:str, encoding:str, data:DataFrame|dict[str, DataFrame], mode:str = 'w'):
        DataFrameData(data=data)
        if isinstance(data, DataFrame):
            data.fillna(NA).to_excel(file_path, index=False)
            return
        with ExcelWriter(file_path) as writer:
            for sheetname, df in data.items():
                df.fillna(NA).to_excel(writer, sheet_name=sheetname, index=False)