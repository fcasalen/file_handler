from pandas import DataFrame
from .json_handler import JsonHandler
from .txt_handler import TxtHandler
from .excel_handler import ExcelHandler
from .pdf_handler import PDFHandler
from .ppt_handler import PPTHandler
from .validators import StringData, FilePaths, FileHanderData
from .utils import get_ext

decider = {
    '.txt': TxtHandler,
    '.json': JsonHandler,
    '.xlsx': ExcelHandler,
    '.pdf': PDFHandler,
    '.ppt': PPTHandler,
    '.pptx': PPTHandler
}

class FileHandler:
    def load(file_paths:str|list[str], encoding:str = 'utf-8', load_first_value:bool = False):
        """
        will load files in a nested dictionary like this:

        {
            file_path_0: data_dict_0,
            file_path_1: ...
        }

        and the data_dicts are like this:

        {
            item_0: item_0_data,
            item_1: item_1_data
        }
        
        For excel files, items will be sheetnames and data their dataframes
        
        For slides and pdfs, items will be slide number and data their text
        
        For json and txt files, items will have only one key(Unique) and data their data"

        If `load_first_value` will load item_0_data, which will be the original data from txt and json files, or the first slide, sheet or page in ppt, xls and pdf files
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        FilePaths(file_paths=file_paths)
        StringData(data=encoding)
        data = {
            file_path: decider[get_ext(file_path=file_path, valid_keys=decider)].load(
                file_path=file_path,
                encoding=encoding,
            ) for file_path in file_paths
        }
        if load_first_value:
            first_value:dict = list(data.values())[0]
            data = list(first_value.values())[0]
        return data
    
    def write(file_handler_data:dict[str, dict[str, str|dict|DataFrame]], encoding:str = 'utf-8'):
        """
        will write files as indicading in `file_handler_data` that needs to be a nested diciontary like this:

        {
            file_path_0: data_dict_0,
            file_path_1: ...
        }

        and the data_dicts should be like this:

        {
            item_0: item_0_data,
            item_1: item_1_data
        }
        
        For excel files, items should be sheetnames and data their dataframes
        
        For slides and pdfs, this package isn't writing data yet (it will print a message stating that)
        
        For json and txt files, items should have only one key(Unique) and data their data

        If json files have more than one item key or not the key Unique, then the data_dict will be consider the data itself

        If txt files have more than one item key or not the key Unique, the data will be transformed in string like this:

        "item_0
        
        item_data_0

        item_1
        
        item_data_1"

        """
        FileHanderData(data=file_handler_data)
        StringData(data=encoding)
        for file_path, data_dict in file_handler_data.items():
            ext = get_ext(file_path=file_path, valid_keys=decider)
            return decider[ext].write(
                file_path=file_path,
                encoding=encoding,
                data=data_dict
            )