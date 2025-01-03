from . import utils
import pytest
from unittest.mock import patch, mock_open, call
from datetime import datetime

def test_get_ext():
    valid_keys = {'.json': 'application/json', '.txt': 'text/plain'}
    assert utils.get_ext('file.JSON', valid_keys) == '.json'
    assert utils.get_ext('file.txt', valid_keys) == '.txt'
    assert utils.get_ext('file.doc', valid_keys) == '.txt'

def test_serialize_datetime():
    dt = datetime(2023, 10, 5, 15, 30, 45)
    assert utils.serialize_datetime(dt) == '2023-10-05T15:30:45'
    data = {'date': dt, 'list': [dt, 'text']}
    expected = {'date': '2023-10-05T15:30:45', 'list': ['2023-10-05T15:30:45', 'text']}
    assert utils.serialize_datetime(data) == expected

def test_deserialize_datetime():
    dt_str = '2023-10-05T15:30:45'
    assert utils.deserialize_datetime(dt_str) == datetime(2023, 10, 5, 15, 30, 45)
    data = {'date': dt_str, 'list': [dt_str, 'text']}
    expected = {'date': datetime(2023, 10, 5, 15, 30, 45), 'list': [datetime(2023, 10, 5, 15, 30, 45), 'text']}
    assert utils.deserialize_datetime(data) == expected
    invalid_str = 'not-a-datetime'
    assert utils.deserialize_datetime(invalid_str) == invalid_str

def test_error_loading():
    file_path = 'example.txt'
    error = Exception('Sample error')
    expected = {"Unique": f"Couldn't load the file {file_path}\n\nError: {str(error)}"}
    assert utils.error_loading(file_path, error) == expected

def test_adjust_phrases():
    # Test text with joined lines
    text = "This is a sentence\nthat continues on the next line.\nAnother sentence starts here."
    expected = "This is a sentence that continues on the next line.\nAnother sentence starts here."
    assert utils.adjust_phrases(text) == expected

    # Test text with proper breaks
    text = "This is a sentence.\n\nAnother sentence starts here."
    expected = "This is a sentence.\n\nAnother sentence starts here."
    assert utils.adjust_phrases(text) == expected

    # Test text with hyphenated words
    text = "This is a hyphen-\nated word."
    expected = "This is a hyphenated word."
    assert utils.adjust_phrases(text) == expected

@patch("builtins.open", new_callable=mock_open)
@patch("time.sleep")
def test_verify_file_is_accessible_success(mock_sleep, mock_open_file):
    """
    Test that the function successfully accesses a file without errors.
    """
    utils.verify_file_is_accessible("valid_file.txt")
    mock_open_file.assert_called_once_with("valid_file.txt", mode="r")
    mock_sleep.assert_not_called() 

@patch("builtins.open", side_effect=PermissionError)
@patch("time.sleep")
def test_verify_file_is_accessible_permission_error(mock_sleep, mock_open_file):
    """
    Test that the function retries when a PermissionError occurs.
    """
    mock_open_file.side_effect = [PermissionError, mock_open().return_value]
    utils.verify_file_is_accessible("inaccessible_file.txt")
    assert mock_open_file.call_count == 2
    mock_sleep.assert_called_once_with(2)


@patch("builtins.open", side_effect=Exception("Unexpected error"))
@patch("time.sleep")
def test_verify_file_is_accessible_unexpected_error(mock_sleep, mock_open_file):
    """
    Test that the function raises a ValueError when an unexpected error occurs.
    """
    with pytest.raises(ValueError, match="Unexpected error"):
        utils.verify_file_is_accessible("error_file.txt")
    mock_open_file.assert_called_once_with("error_file.txt", mode="r")
    mock_sleep.assert_not_called() 

@patch("builtins.open", side_effect=PermissionError)
@patch("time.sleep")
def test_verify_file_is_accessible_indefinite_permission_error(mock_sleep, mock_open_file):
    """
    Test that the function loops 11 times on repeated PermissionErrors.
    """
    mock_open_file.side_effect = [PermissionError] * 11 + [mock_open().return_value]
    utils.verify_file_is_accessible("inaccessible_file.txt")
    assert mock_open_file.call_count == 12
    all_calls = mock_sleep.call_args_list
    assert all_calls.count(call(2)) == 10
    assert all_calls.count(call(4)) == 1

