from pathlib import Path

import pandas as pd


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> dict[str, pd.DataFrame]:
    """Load dataframes from a xls or xlsx file using pandas.read_excel method

    Args:
        file_path (Path): the path to the file
        password (str): the password to be used (not implemented). Defaults to None.
        encoding (str, optional): encoding to be used (not implemented). Defaults to
            "utf-8".
        mode (str, optional): mode to be used (not implemented). Defaults to "r".

    :returns: dictionary where keys are the sheetnames and values
        the dataframes
    :rtype: dict[str, pd.DataFrame]
    """
    df_dict = pd.read_excel(file_path, sheet_name=None)
    for sht in df_dict:
        df_dict[sht] = df_dict[sht].fillna(pd.NA).convert_dtypes()
    return df_dict


def write(
    file_path: str | Path,
    data: pd.DataFrame | dict[str, pd.DataFrame],
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Write a dataframe or a dictionary of dataframes to a xlsx file

    Args:
        file_path (str | Path): the path to the file
        data (pd.DataFrame | dict[str, pd.DataFrame]): the dataframe (or
            dictionary of dataframes) to be written
        password (str): the password to be used (not implemented). Defaults to None.
        encoding (str, optional): encoding to be used (not implemented)
        mode (str, optional): the mode to be used (not implemented)
    """
    if isinstance(data, pd.DataFrame):
        data.fillna(pd.NA).convert_dtypes().to_excel(file_path, index=False)
        return
    with pd.ExcelWriter(file_path) as writer:
        for sheetname, df in data.items():
            df.fillna(pd.NA).convert_dtypes().to_excel(
                writer, sheet_name=sheetname, index=False
            )
