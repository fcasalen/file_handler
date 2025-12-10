from pathlib import Path

import pandas as pd

from src.file_handler import excel_handler


def test_write_single_dataframe(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "single_dataframe.xlsx"
    excel_handler.write(file_path=file_path, encoding="utf-8", data=df)
    loaded_dict = pd.read_excel(file_path, sheet_name=None)
    pd.testing.assert_frame_equal(loaded_dict["Sheet1"], df.fillna(pd.NA))
    assert list(loaded_dict.keys()) == ["Sheet1"]


def test_write_single_dataframe_with_name(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "single_dataframe_named.xlsx"
    excel_handler.write(file_path=file_path, encoding="utf-8", data={"Data": df})
    loaded_dict = pd.read_excel(file_path, sheet_name=None)
    pd.testing.assert_frame_equal(loaded_dict["Data"], df.fillna(pd.NA))
    assert list(loaded_dict.keys()) == ["Data"]


def test_write_multiple_dataframes(tmp_path: Path):
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"C": [5, 6], "D": [7, 8]})
    data = {"First": df1, "Second": df2}
    file_path = tmp_path / "multiple_dataframes.xlsx"
    excel_handler.write(file_path=file_path, encoding="utf-8", data=data)
    loaded_dict = pd.read_excel(file_path, sheet_name=None)
    pd.testing.assert_frame_equal(loaded_dict["First"], df1.fillna(pd.NA))
    pd.testing.assert_frame_equal(loaded_dict["Second"], df2.fillna(pd.NA))
    assert list(loaded_dict.keys()) == ["First", "Second"]


def test_load_dataframe(tmp_path: Path):
    df = pd.DataFrame({"X": [10, 20], "Y": [30, None]})
    file_path = tmp_path / "load_test.xlsx"
    df.to_excel(file_path, index=False)
    loaded_dict = excel_handler.load(file_path)
    pd.testing.assert_frame_equal(
        loaded_dict["Sheet1"], df.convert_dtypes().fillna(pd.NA)
    )
    assert list(loaded_dict.keys()) == ["Sheet1"]


def test_load_multiple_sheets(tmp_path: Path):
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, None]})
    df2 = pd.DataFrame({"C": [5, None], "D": [7, 8]})
    file_path = tmp_path / "multiple_sheets_test.xlsx"
    with pd.ExcelWriter(file_path) as writer:
        df1.to_excel(writer, sheet_name="First", index=False)
        df2.to_excel(writer, sheet_name="Second", index=False)
    loaded_dict = excel_handler.load(file_path)
    pd.testing.assert_frame_equal(
        loaded_dict["First"], df1.convert_dtypes().fillna(pd.NA)
    )
    pd.testing.assert_frame_equal(
        loaded_dict["Second"], df2.convert_dtypes().fillna(pd.NA)
    )
    assert list(loaded_dict.keys()) == ["First", "Second"]


def test_round_trip(tmp_path: Path):
    df_original = pd.DataFrame({"M": [100, None, 300], "N": [400, 500, None]})
    file_path = tmp_path / "integration_test.xlsx"
    excel_handler.write(file_path=file_path, encoding="utf-8", data=df_original)
    loaded_dict = excel_handler.load(file_path)
    pd.testing.assert_frame_equal(
        loaded_dict["Sheet1"], df_original.convert_dtypes().fillna(pd.NA)
    )
    assert list(loaded_dict.keys()) == ["Sheet1"]
