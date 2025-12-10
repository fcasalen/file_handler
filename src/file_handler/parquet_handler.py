from pathlib import Path

import pandas as pd


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> pd.DataFrame:
    """Load a dataframe from a parquet file using pandas.read_parquet method

    Args:
        file_path (Path): the path to the file
        password (str): the password to be used (not implemented). Defaults to None.
        encoding (str, optional): encoding to be used (not implemented). Defaults
            to "utf-8".
        mode (str, optional): mode to be used (not implemented). Defaults to "r".

    Returns:
        pd.DataFrame: the dataframe from the file
    """
    return pd.read_parquet(file_path).fillna(pd.NA)


def write(
    file_path: str | Path,
    data: pd.DataFrame,
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Write a dataframe to a parquet file

    Args:
        file_path (str | Path): the path to the file
        data (pd.DataFrame): the dataframe to be written
        password (str, optional): the password to be used (not implemented).
            Defaults to None.
        encoding (str, optional): encoding to be used (not implemented). Defaults
            to "utf-8".
        mode (str, optional): the mode to be used (not implemented). Defaults to "w".
    """
    data.fillna(pd.NA).to_parquet(file_path, index=False)
