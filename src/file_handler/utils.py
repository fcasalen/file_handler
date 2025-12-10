import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any


def serialize_datetime(obj: Any) -> Any:
    """Recursively serialize datetime objects to ISO format strings.

    Args:
        obj (Any): The object to serialize.

    Returns:
        Any: The serialized object.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    else:
        return obj


def deserialize_datetime(obj: Any) -> Any:
    """Recursively deserialize ISO format strings to datetime objects.

    Args:
        obj (Any): The object to deserialize.

    Returns:
        Any: The deserialized object.
    """

    if isinstance(obj, str):
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return obj
    elif isinstance(obj, dict):
        return {
            deserialize_datetime(k): deserialize_datetime(v) for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [deserialize_datetime(item) for item in obj]
    else:
        return obj


def adjust_phrases(page_text: str):
    lines = page_text.split("\n")
    joined_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].strip()
        if current_line != "" and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            while (
                not (
                    current_line.endswith((".", "!", "?"))
                    and re.match(r'^[A-Z0-9"“]', next_line)
                )
                and i < len(lines) - 2
                and next_line != ""
            ):
                if current_line[-1] != "-":
                    current_line += " " + next_line
                else:
                    if not next_line[0].isdigit():
                        current_line = current_line[:-1]
                    current_line += next_line
                i += 1
                next_line = lines[i + 1].strip()
        joined_lines.append(current_line)
        i += 1
    text = re.sub(r"\n\n+", "\n\n", "\n".join(joined_lines))
    text = re.sub(r"-\n\n", "", text)
    text = re.sub(r"-\n", "", text)
    text = re.sub(" +", " ", text)
    text = re.sub("\n ", "\n", text)
    text = re.sub(" \n", "\n", text)
    if text != "":
        while text[-1] == "\n":
            text = text[:-1]
    return text


def verify_file_is_accessible(file_path: Path, time_step: int = 5) -> bool:
    """Verify if a file is accessible, retrying 10 times if necessary.

    Args:
        file_path (str): Path to the file to check.
        time_step (int, optional): Base time to wait between retries. Defaults to 5.

    Raises:
        Exception: If an unexpected error occurs.

    Returns:
        bool: True if the file is accessible, False otherwise.
    """
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            if file_path.exists() is False:
                return True
            with open(file_path, mode="r"):
                pass
            return True
        except PermissionError:
            print(
                f"File {file_path} is unaccessible. Verify! We will try again in "
                f"{time_step} seconds (already tried {retries + 1} times)!"
            )
            time.sleep(time_step)
            retries += 1
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    return False
