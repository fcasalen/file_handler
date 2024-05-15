from pandas import DataFrame
from tqdm import tqdm
from .json_handler import JsonHandler
from .txt_handler import TxtHandler
from .excel_handler import ExcelHandler
from .pdf_handler import PDFHandler
from .ppt_handler import PPTHandler
from .validators import StringData, FilePaths, FileHanderData
from .utils import get_ext, deserialize_datetime

decider = {
    '.txt': TxtHandler,
    '.json': JsonHandler,
    '.xlsx': ExcelHandler,
    '.pdf': PDFHandler,
    '.ppt': PPTHandler,
    '.pptx': PPTHandler
}

class FileHandler:
    @staticmethod
    def load(file_paths:str|list[str], encoding:str = 'utf-8', mode:str = 'r', load_first_value:bool = False, progress_bar:bool = True):
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

        `mode` should be r or rb and it only affects json and txt files

        if extension is not txt, json, xlsx, ppt, pptx or pdf, will treat as txt file
        
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        FilePaths(file_paths=file_paths)
        StringData(data=encoding)
        data = {
            file_path: decider[get_ext(file_path=file_path, valid_keys=decider)].load(
                file_path=file_path,
                encoding=encoding,
                mode = mode
            ) for file_path in tqdm(file_paths, desc='Loading data...', disable=not progress_bar)
        }
        if load_first_value:
            first_value:dict = list(data.values())[0]
            data = list(first_value.values())[0]
        return data
    
    @staticmethod
    def write(file_handler_data:dict[str, dict[str, str|dict|DataFrame]], encoding:str = 'utf-8', mode:str = 'w', progress_bar:bool = True):
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
        
        `mode` should be w or wb and it only affects json and txt files

        if extension is not txt, json, xlsx, ppt, pptx or pdf, will treat as txt file

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
        for file_path, data_dict in tqdm(file_handler_data.items(), desc='LWriting data...', disable=not progress_bar):
            ext = get_ext(file_path=file_path, valid_keys=decider)
            return decider[ext].write(
                file_path=file_path,
                encoding=encoding,
                data=data_dict,
                mode=mode
            )
        
    def deserialize_datetimes_in_json(json:dict):
        "json files don't accept datetime object, so they are saved converting datetime objects in string in isoformat. This method converts strings that matchs isoformat to a datetime back again"
        return deserialize_datetime(json)