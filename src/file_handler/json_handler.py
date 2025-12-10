import json
from pathlib import Path

from .utils import deserialize_datetime, serialize_datetime


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> list | dict:
    """Load a json file

    Args:
        file_path (Path): the path to the file
        password (str): the password to be used (not implemented).
            Defaults to None.
        encoding (str, optional): encoding to be used. Defaults to "utf-8".
        mode (str, optional): mode to be used. Defaults to "r".

    :returns: the data loaded from the json file
    :rtype: list | dict
    """
    with open(file_path, mode=mode, encoding=encoding) as f:
        data = json.load(f)
    return deserialize_datetime(data)


def write(
    file_path: str | Path,
    data: list | dict,
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Write data to a json file

    Args:
        file_path (str | Path): the path to the file
        data (list | dict): the data to be written
        password (str, optional): the password to be used (not implemented).
            Defaults to None.
        encoding (str, optional): encoding to be used. Defaults to "utf-8".
        mode (str, optional): the mode to be used. Defaults to "w".
    """
    data = serialize_datetime(data)
    with open(file_path, mode=mode, encoding=encoding) as f:
        json.dump(data, f, indent=4)
