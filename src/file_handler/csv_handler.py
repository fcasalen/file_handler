from pathlib import Path

import pandas as pd


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> pd.DataFrame:
    """Load a dataframe from a csv file using pandas.read_csv method

    Args:
        file_path (Path): the path to the file
        password (str): the password to be used (not implemented). Defaults to None.
        encoding (str, optional): encoding to be used (not implemented). Defaults
            to "utf-8".
        mode (str, optional): mode to be used (not implemented). Defaults to "r".

    Returns:
        pd.DataFrame: the dataframe from the file
    """
    return pd.read_csv(file_path).convert_dtypes()


def write(
    file_path: Path,
    data: pd.DataFrame,
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Write a dataframe do csv file.

    Args:
        file_path (str | Path): the path to the file
        data (pd.DataFrame): the dataframe to be written
        password (str): the password to be used (not implemented). Defaults to None.
        encoding (str, optional): encoding to be used (not implemented)
        mode (str, optional): the mode to be used (not implemented)
    """
    data.fillna(pd.NA).convert_dtypes().to_csv(file_path, index=False)
