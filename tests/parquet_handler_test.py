from pathlib import Path

import pandas as pd

from src.file_handler import parquet_handler


def test_write_single_dataframe(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "single_dataframe.parquet"
    parquet_handler.write(file_path=file_path, encoding="utf-8", data=df)
    loaded_df = pd.read_parquet(file_path)
    pd.testing.assert_frame_equal(loaded_df, df.fillna(pd.NA))


def test_write_dataframe(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "df.parquet"
    parquet_handler.write(file_path=file_path, encoding="utf-8", data=df)
    assert file_path.exists()


def test_round_trip(tmp_path: Path):
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
    file_path = tmp_path / "round_trip.parquet"
    parquet_handler.write(file_path=file_path, data=df)
    loaded_df = parquet_handler.load(file_path=file_path)
    pd.testing.assert_frame_equal(loaded_df, df.fillna(pd.NA))
