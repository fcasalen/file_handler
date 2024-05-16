from pandas import DataFrame
from tqdm import tqdm
from multiprocess import Pool
from functools import partial
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

def loader(file_path_with_password:tuple[str, str], encoding:str, mode:str):
    return decider[get_ext(file_path=file_path_with_password[0], valid_keys=decider)].load(
        file_path_with_password=file_path_with_password,
        encoding=encoding,
        mode = mode
    )

def writer(file_hander_data_items:tuple, encoding:str, mode:str):
    file_path, data_dict = file_hander_data_items
    decider[get_ext(file_path=file_path, valid_keys=decider)].write(
        file_path=file_path,
        encoding=encoding,
        data=data_dict,
        mode=mode
    )

class FileHandler:
    @staticmethod
    def load(file_paths:str|list[str]|dict[str, str], encoding:str = 'utf-8', mode:str = 'r', load_first_value:bool = False, progress_bar:bool = True, multiprocess:bool = False):
        """
        `file_paths` should be a dic with keys as the paths for the files and the values as the passwords for the files.
        
        If `file_paths` is string, it will be treated as a unique path with no password.
        
        If `file_paths` is a list, it will be consider as a list of paths with no password.
        
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

        `progress_bar` True or False to show a progress_bar while executing

        `multiprocess` True or False to use multiprocessing to speed up execution (increases overhead, so this will speed the overall execution only if a bunch of files are being processed)

        if extension is not txt, json, xlsx, ppt, pptx or pdf, will treat as txt file
        
        """
        if isinstance(file_paths, str):
            file_paths = {file_paths: None}
        if isinstance(file_paths, list):
            file_paths = {f:None for f in file_paths}
        FilePaths(file_paths=file_paths)
        StringData(data=encoding)
        if multiprocess:
            with Pool() as p:
                results = list(
                    tqdm(
                        p.imap(partial(loader, encoding=encoding, mode=mode), file_paths.items()),
                        disable=not progress_bar,
                        total=len(file_paths),
                        desc='Loading data...'
                    )
                )
            data = {file_path:result for file_path, result in zip(file_paths, results)}
        else:
            data = {
            file_path_with_password[0]: loader(
                file_path_with_password=file_path_with_password,
                encoding=encoding,
                mode = mode
            ) for file_path_with_password in tqdm(
                file_paths.items(),
                disable=not progress_bar,
                desc='Loading data...'
            )
        }
        if load_first_value:
            first_value:dict = list(data.values())[0]
            data = list(first_value.values())[0]
        return data
    
    @staticmethod
    def write(file_handler_data:dict[str, dict[str, str|dict|DataFrame]], encoding:str = 'utf-8', mode:str = 'w', progress_bar:bool = True, multiprocess:bool = False):
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
        if multiprocess:
            with Pool() as p:
                list(
                    tqdm(
                        p.imap(partial(writer, encoding=encoding, mode=mode), file_handler_data.items()),
                        disable=not progress_bar,
                        total=len(file_handler_data),
                        desc='Writing data...'
                    )
                )
        else:
            [
                writer((file_path, file_path_data), mode=mode, encoding=encoding) for file_path, file_path_data in tqdm(
                    file_handler_data.items(),
                    desc='Writing data...',
                    disable=not progress_bar)
            ]
        
    def deserialize_datetimes_in_json(json:dict):
        "json files don't accept datetime object, so they are saved converting datetime objects in string in isoformat. This method converts strings that matchs isoformat to a datetime back again"
        return deserialize_datetime(json)

# from multiprocess import Pool
# from pandas import read_excel
# from os import listdir
# from os.path import join
# from functools import partial
# from tqdm import tqdm



# path = r'C:\Users\bes8\OneDrive - PETROBRAS\BDOC GR\Desenvolvimento\Painéis em Power BI\PG_GR - Cronoweb - Visão SM-PG-GR\Cronoweb'
# file_paths = [join(path, k) for k in listdir(path)]

# def read_file(file, sheet_name):
#     return read_excel(file, sheet_name=sheet_name)

# pool = Pool()
# results = tqdm(pool.imap(partial(read_excel, sheet_name=None), file_paths))
# pool.close()