from pathlib import Path

import pandas as pd

from src.file_handler import csv_handler


def test_write_single_dataframe(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "single_dataframe.csv"
    csv_handler.write(file_path=file_path, encoding="utf-8", data=df)
    loaded_df = pd.read_csv(file_path).convert_dtypes().fillna(pd.NA)
    pd.testing.assert_frame_equal(loaded_df, df.convert_dtypes().fillna(pd.NA))


def test_load_dataframe(tmp_path: Path):
    df = pd.DataFrame({"X": [10, 20], "Y": [30, None]}).convert_dtypes()
    file_path = tmp_path / "load_test.csv"
    df.convert_dtypes().to_csv(file_path, index=False)
    loaded = csv_handler.load(file_path)
    pd.testing.assert_frame_equal(loaded, df.fillna(pd.NA))


def test_round_trip(tmp_path: Path):
    df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
    file_path = tmp_path / "df.csv"
    csv_handler.write(file_path=file_path, encoding="utf-8", data=df)
    loaded = csv_handler.load(file_path)
    pd.testing.assert_frame_equal(loaded, df)
