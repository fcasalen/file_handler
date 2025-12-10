from pathlib import Path


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> str | bytes:
    """Load text file.

    Args:
        file_path (Path): path to the text file.
        password (str, optional): password to open the file (not implemented).
            Defaults to None.
        encoding (str, optional): encoding type. Defaults to "utf-8".
        mode (str, optional): file mode. Defaults to 'r'.

    :returns: content of the text file.
    :rtype: str | bytes
    """

    with open(file_path, mode=mode, encoding=encoding) as f:
        data = f.read()
    return data


def write(
    file_path: str,
    data: str | bytes,
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Write string or bytes to a txt file.

    Args:
        file_path (str): path to the txt file.
        data (str | bytes): data to write.
        password (str, optional): password to encrypt the file (not implemented).
            Defaults to None.
        encoding (str, optional): encoding type. Defaults to "utf-8".
        mode (str, optional): file mode. Defaults to 'w'.
    """
    with open(file_path, mode=mode, encoding=encoding) as f:
        f.write(data)
