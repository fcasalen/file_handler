from os.path import splitext
from datetime import datetime
import time
import re

def get_ext(file_path:str, valid_keys:dict):
    _,ext = splitext(file_path.lower())
    if ext not in valid_keys:
        ext = '.txt'
    return ext

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    else:
        return obj

def deserialize_datetime(obj):
    if isinstance(obj, str):
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return obj
    elif isinstance(obj, dict):
        return {deserialize_datetime(k): deserialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deserialize_datetime(item) for item in obj]
    else:
        return obj
    
def error_loading(file_path:str, error:Exception):
    return {"Unique": f"Couldn't load the file {file_path}\n\nError: {str(error)}"}

def adjust_phrases(page_text:str):
    lines = page_text.split('\n')
    joined_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].strip()
        if current_line != '' and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            while not (current_line.endswith(('.', '!', '?')) and re.match(r'^[A-Z0-9"“]', next_line)) and i < len(lines) - 2 and next_line != '':
                if current_line[-1] != '-':
                    current_line += ' ' + next_line
                else:
                    if not next_line[0].isdigit():
                        current_line = current_line[:-1]
                    current_line += next_line
                i += 1
                next_line = lines[i + 1].strip()
        joined_lines.append(current_line)
        i += 1
    text = re.sub(r"\n\n+", "\n\n", '\n'.join(joined_lines))
    text = re.sub(r"-\n\n", "", text)
    text = re.sub(r"-\n", "", text)
    text = re.sub(" +", ' ', text)
    text = re.sub('\n ', '\n', text)
    text = re.sub(' \n', '\n', text)
    if text != '':
        while text[-1] == '\n':
            text = text[:-1]
    return text

def verify_file_is_accessible(file_path:str):
    """
    Verify if a file is accessible, retrying in case of PermissionError.

    Args:
        file_path (str): Path to the file to check.
    """
    acessible = False
    retries = 0
    while not acessible:
        try:
            with open(file_path, mode='r'):
                pass
            acessible = True
        except PermissionError:
            new_time_sleep = (retries // 10) * 2 + 2
            print(f'File {file_path} is unaccessible. Verify! We will try again in {new_time_sleep} seconds (already tried {retries + 1} times)!')
            time.sleep(new_time_sleep)
            retries += 1
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")