from pandas import DataFrame
from .parquet_handler import ParquetHandler
import os

def test_all():
    df = DataFrame({'Col1': [0,1]})
    data = {'Unique': df}
    file_path = os.path.join(os.path.dirname(__file__), 'parquet_handler_test.parquet')
    ParquetHandler.write(file_path=file_path, encoding='utf-8', data=data)
    load_dict = ParquetHandler.load(file_path_with_password=(file_path, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df)
    df2 =  DataFrame({'Col1': [2,3]})
    data = {
        'Sheet1': df,
        "Sheet2": df2
    }
    ParquetHandler.write(file_path=file_path, encoding='utf-8', data=data)
    file_path_sheet1 = os.path.join(os.path.dirname(__file__), 'parquet_handler_test_Sheet1.parquet')
    load_dict = ParquetHandler.load(file_path_with_password=(file_path_sheet1, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df)
    file_path_sheet2 = os.path.join(os.path.dirname(__file__), 'parquet_handler_test_Sheet2.parquet')
    load_dict = ParquetHandler.load(file_path_with_password=(file_path_sheet2, None), encoding='utf-8')
    assert list(load_dict.keys()) == ['Unique']
    assert load_dict['Unique'].equals(df2)
    os.remove(file_path)
    os.remove(file_path_sheet1)
    os.remove(file_path_sheet2)
    ParquetHandler.write(file_path=file_path, encoding='utf-8', data=df)
    assert os.path.exists(file_path)
    new_df = ParquetHandler.load((file_path, None), encoding='utf-8')
    assert df.equals(new_df['Unique'])
    os.remove(file_path)

    