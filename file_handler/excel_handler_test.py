from os.path import dirname, join
from os import remove
from pandas import DataFrame
from .excel_handler import ExcelHandler

def test_all():
    df = DataFrame({'Col1': [0,1]})
    data = {'Sheet1': df}
    file_path = join(dirname(__file__), 'excel_handler_test.xlsx')
    ExcelHandler.write(file_path=file_path, encoding='utf-8', data=data)
    load_dict = ExcelHandler.load(file_path=file_path, encoding='utf-8')
    assert list(load_dict.keys()) == ['Sheet1']
    assert load_dict['Sheet1'].equals(df)
    df2 =  DataFrame({'Col1': [2,3]})
    data = {
        'Sheet1': df,
        "Sheet2": df2
    }
    ExcelHandler.write(file_path=file_path, encoding='utf-8', data=data)
    load_dict = ExcelHandler.load(file_path=file_path, encoding='utf-8')
    assert list(load_dict.keys()) == ['Sheet1', 'Sheet2']
    assert load_dict['Sheet1'].equals(df)
    assert load_dict['Sheet2'].equals(df2)
    remove(file_path)
    