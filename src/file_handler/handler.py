import sys
from functools import partial
from pathlib import Path
from typing import Any, Protocol

import pandas as pd
from loguru import logger
from multiprocess import pool
from tqdm import tqdm

from . import (
    csv_handler,
    excel_handler,
    json_handler,
    parquet_handler,
    pdf_handler,
    ppt_handler,
    txt_handler,
    utils,
)

logger.remove()
logger.add(Path(__file__).parent / "error.log", level="INFO", enqueue=True)
logger.add(sys.stderr, level="INFO")

decider = {
    ".txt": txt_handler,
    ".json": json_handler,
    ".xlsx": excel_handler,
    ".pdf": pdf_handler,
    ".ppt": ppt_handler,
    ".pptx": ppt_handler,
    ".csv": csv_handler,
    ".parquet": parquet_handler,
}


class Handlers(Protocol):
    @staticmethod
    def load(
        file_path: Path, password: str, encoding: str, mode: str
    ) -> str | bytes | list | dict[str, str | dict | pd.DataFrame] | pd.DataFrame: ...

    @staticmethod
    def write(
        file_path: Path,
        data: str | bytes | list | dict | pd.DataFrame,
        password: str,
        encoding: str,
        mode: str,
    ): ...


def get_decider(file_path: Path, mode: str) -> Handlers:
    """Function to decide which handler to use based on file extension and mode.

    Args:
        file_path (Path): Path to the file.
        mode (str): Mode in which the file is to be handled.

    Returns:
        Handlers: The appropriate handler class for the file.
    """
    ext = file_path.suffix.lower()
    if ext not in decider or "b" in mode:
        ext = ".txt"
    return decider[ext]


def loader(
    file_path: Path, password: str, encoding: str, mode: str
) -> str | bytes | list | dict | pd.DataFrame:
    """Loader function to load a file using the appropriate handler.

    Args:
        file_path (str): Path to the file.
        password (str): Password for the file if needed.
        encoding (str): Encoding to use for loading the file.
        mode (str): Mode in which the file is to be handled.

    Returns:
        (str | bytes | list | dict | pd.DataFrame): The loaded data from the file.
    """
    try:
        return get_decider(file_path=Path(file_path), mode=mode).load(
            file_path=file_path, password=password, encoding=encoding, mode=mode
        )
    except Exception as e:
        logger.exception(f"Error loading file {file_path}: {str(e)}")
        logger.info("\n\n---\n\n")
        return f"Error loading file {file_path}: {str(e)}"


def writer(
    file_path: Path,
    data: str | bytes | list | dict | pd.DataFrame,
    password: str,
    encoding: str,
    mode: str,
) -> None:
    """Writer function to write data to a file using the appropriate handler.

    Args:
        file_path (Path): path to the file.
        data (str | bytes | list | dict | pd.DataFrame): Data to be written to the file.
        password (str): Password for the file if needed.
        encoding (str): Encoding to use for writing the file.
        mode (str): Mode in which the file is to be handled.
    """
    try:
        if utils.verify_file_is_accessible(file_path):
            get_decider(file_path=file_path, mode=mode).write(
                file_path=file_path,
                data=data,
                password=password,
                encoding=encoding,
                mode=mode,
            )
            return True
        return f"File {str(file_path)} is not accessible for writing."
    except Exception as e:
        logger.exception(f"Error writing file {file_path}: {str(e)}")
        logger.info("\n\n---\n\n")
        return f"Error writing file {file_path}: {str(e)}"


class FileHandler:
    @staticmethod
    def load(
        file_paths: str | list[str] | dict[str, str],
        encoding: str = "utf-8",
        mode: str = "r",
        progress_bar: bool = True,
        multiprocess: bool = False,
    ) -> dict[str | bytes | list | dict | pd.DataFrame]:
        """Load txt, json, xls, xlsx, parquet, csv, ppt, pttx or pdf files as indicating
        in `file_paths`.

        If extension is none of the above, will treat as txt file.

        If `mode` has 'b', will treat as txt file.


        Args:
            file_paths (str | list[str] | dict[str, str]):
                - if string, will load only one file without password
                - if list, will load all files in the list without password
                - if dict, will load all files in the dict where the values in the
                    dict are password (only valid for pdfs)
            encoding (str, optional): encoding to load the files and will only work
                for json and txt files. Defaults to 'utf-8'.
            mode (str, optional): mode to load the files and will only work for json
                and txt files. Defaults to 'r'.
            progress_bar (bool, optional): progress bar to indicate the progress.
                Defaults to True.
            multiprocess (bool, optional): multiprocess option to handle lots of or
                big files. Defaults to False.

        :returns: where keys are filepaths and values are data loaded from the files

            - For excel files, data will be a dict[sheetnames, pandas.DataFrame]

            - For slides and pdfs, data will be a dict[slide_number, slide text]

            - For json files, data will be a dict or list as in the json file

            - For txt files, data will be a string with the text content

            - for parquet and csv files, data will be a pandas.DataFrame

            - for any error loading a file, value will be a string with the error
                message

            - for mode with 'b', data will be bytes
        :rtype: dict[str | bytes | list | dict | pd.DataFrame]
        """
        if isinstance(file_paths, str) or isinstance(file_paths, Path):
            file_paths: dict[Path, str] = {Path(file_paths): None}
        elif isinstance(file_paths, list):
            file_paths: dict[Path, str] = {Path(f): None for f in file_paths}
        elif isinstance(file_paths, dict):
            file_paths: dict[Path, str] = {Path(k): v for k, v in file_paths.items()}
        else:
            raise AssertionError(
                "file_paths should be str, list[str] or dict[str, str]"
            )
        assert all(file.exists() for file in file_paths.keys()), (
            "all file paths should exist"
        )
        assert all(isinstance(v, (str, type(None))) for v in file_paths.values()), (
            "password values should be str or None"
        )
        if "b" in mode:
            encoding = None
        if multiprocess:
            with pool.Pool() as p:
                results = list(
                    tqdm(
                        p.starmap(
                            partial(loader, encoding=encoding, mode=mode),
                            file_paths.items(),
                        ),
                        disable=not progress_bar,
                        total=len(file_paths),
                        desc="Loading data...",
                    )
                )
            return {
                str(file_path): result for file_path, result in zip(file_paths, results)
            }
        return {
            str(file_path): loader(
                file_path=file_path, password=password, encoding=encoding, mode=mode
            )
            for file_path, password in tqdm(
                file_paths.items(), disable=not progress_bar, desc="Loading data..."
            )
        }

    @staticmethod
    def write(
        file_handler_data: dict[
            str, str, bytes | list | pd.DataFrame | dict[str, str | pd.DataFrame | Any]
        ],
        encoding: str = "utf-8",
        mode: str = "w",
        progress_bar: bool = True,
        multiprocess: bool = False,
    ) -> dict[str, bool | str]:
        """will write files (without password)

        Args:
            file_handler_data (dict): dict[str, str | bytes | list | pd.DataFrame |
                dict[str, str | pd.DataFrame | Any]])
                - keys are file paths where data should be written
                - values are data to be written to the files
                - if extension is not txt, json, xlsx, ppt, pptx or pdf, will treat as
                    txt file
                - dor excel files, data should pandas.DataFrame or a dictionary with
                    keys as sheetnames and values as pandas.DataFrame.
                - for slides and pdfs, this package isn't writing data yet (it will
                    print a message stating that)
                - for json data should be a dictionary or a list.
                - for txt files, data should be a string or bytes.
            encoding (str, optional): encoding to write the files and will only work for
                json and txt files. Defaults to 'utf-8'.
            mode (str, optional): mode to write the files and will only work for
                json and txt files. Defaults to 'w'. Should be w or wb and it only
                    affects json and txt files
            progress_bar (bool, optional): progress bar to indicate the progress.
                Defaults to True.
            multiprocess (bool, optional): multiprocess option to handle lots of or
                big files. Defaults to False.

        :returns: keys are file paths and values are True if file was written
            successfully or error message if there was an error writing the file
        :rtype: dict[str, bool | str]
        """
        if "b" in mode:
            encoding = None
        assert isinstance(file_handler_data, dict), (
            "file_handler_data should be a dict[str, str | bytes | list | pd.DataFrame "
            "| dict[str, str | pd.DataFrame | Any]]"
        )
        try:
            file_handler_data = {Path(k): v for k, v in file_handler_data.items()}
        except TypeError:
            raise AssertionError(
                "all keys in file_handler_data should be str representing file paths"
            )
        if multiprocess:
            with pool.Pool() as p:
                results = list(
                    tqdm(
                        p.starmap(
                            partial(
                                writer, encoding=encoding, mode=mode, password=None
                            ),
                            file_handler_data.items(),
                        ),
                        disable=not progress_bar,
                        total=len(file_handler_data),
                        desc="Writing data...",
                    )
                )
            return {
                str(file_path): result
                for file_path, result in zip(file_handler_data.keys(), results)
            }
        return {
            str(file_path): writer(
                file_path=file_path,
                data=data,
                password=None,
                encoding=encoding,
                mode=mode,
            )
            for file_path, data in tqdm(
                file_handler_data.items(),
                disable=not progress_bar,
                desc="Writing data...",
            )
        }
