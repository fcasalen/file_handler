from os.path import dirname, join
from os import remove
from pandas import DataFrame
from .csv_handler import CSVHandler

def test_all():
    df = DataFrame({'Col1': [0,1]})
    data = {'Unique': df}
    file_path = join(dirname(__file__), 'csv_handler_test.csv')
    CSVHandler.write(file_path=file_path, encoding='utf-8', data=data)
    load_dict = CSVHandler.load(file_path_with_password=(file_path, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df)
    df2 =  DataFrame({'Col1': [2,3]})
    data = {
        'Sheet1': df,
        "Sheet2": df2
    }
    CSVHandler.write(file_path=file_path, encoding='utf-8', data=data)
    file_path_sheet1 = join(dirname(__file__), 'csv_handler_test_Sheet1.csv')
    load_dict = CSVHandler.load(file_path_with_password=(file_path_sheet1, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df)
    file_path_sheet2 = join(dirname(__file__), 'csv_handler_test_Sheet2.csv')
    load_dict = CSVHandler.load(file_path_with_password=(file_path_sheet2, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df2)
    remove(file_path)
    remove(file_path_sheet1)
    remove(file_path_sheet2)
    