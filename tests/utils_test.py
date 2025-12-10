from datetime import datetime
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.file_handler import utils


class TestSerializeDeserializePath:
    def test_serialize_datetime(self):
        dt = datetime(2023, 10, 5, 15, 30, 45)
        assert utils.serialize_datetime(dt) == "2023-10-05T15:30:45"

    def test_serialize_dict(self):
        dt = datetime(2023, 10, 5, 15, 30, 45)
        data = {"date": dt, "list": [dt, "text"]}
        expected = {
            "date": "2023-10-05T15:30:45",
            "list": ["2023-10-05T15:30:45", "text"],
        }
        assert utils.serialize_datetime(data) == expected

    def test_deserialize_datetime(self):
        dt_str = "2023-10-05T15:30:45"
        assert utils.deserialize_datetime(dt_str) == datetime(2023, 10, 5, 15, 30, 45)

    def test_deserialize_dict(self):
        dt_str = "2023-10-05T15:30:45"
        data = {"date": dt_str, "list": [dt_str, "text"]}
        expected = {
            "date": datetime(2023, 10, 5, 15, 30, 45),
            "list": [datetime(2023, 10, 5, 15, 30, 45), "text"],
        }
        assert utils.deserialize_datetime(data) == expected

    def test_deserialize_invalid_string(self):
        invalid_str = "not-a-datetime"
        assert utils.deserialize_datetime(invalid_str) == invalid_str


def test_adjust_phrases():
    # Test text with joined lines
    text = (
        "This is a sentence\nthat continues on the next line.\nAnother sentence "
        "starts here."
    )
    expected = (
        "This is a sentence that continues on the next line.\nAnother sentence "
        "starts here."
    )
    assert utils.adjust_phrases(text) == expected

    # Test text with proper breaks
    text = "This is a sentence.\n\nAnother sentence starts here."
    expected = "This is a sentence.\n\nAnother sentence starts here."
    assert utils.adjust_phrases(text) == expected

    # Test text with hyphenated words
    text = "This is a hyphen-\nated word."
    expected = "This is a hyphenated word."
    assert utils.adjust_phrases(text) == expected


@patch("time.sleep")
class TestVerifiyFileIsAccessible:
    def test_inexisting_file(self, mock_sleep):
        valid_file = Path("inexisting.txt")
        assert utils.verify_file_is_accessible(valid_file)

    @patch("builtins.open", new_callable=mock_open)
    def test_accessible_success(self, mock_open_file, mock_sleep, tmp_path: Path):
        """
        Test that the function successfully opens an accessible file.
        """
        file_path = tmp_path / "accessible_file.txt"
        file_path.write_text("Test content")
        utils.verify_file_is_accessible(file_path)
        mock_open_file.assert_called_once_with(file_path, mode="r")
        mock_sleep.assert_not_called()

    @patch("builtins.open", side_effect=PermissionError)
    def test_inaccessible_file(self, mock_open_file, mock_sleep, tmp_path: Path):
        """
        Test that the function retries when a PermissionError occurs.
        """
        file_path = tmp_path / "inaccessible_file.txt"
        file_path.write_text("Test content")
        assert utils.verify_file_is_accessible(file_path) is False
        assert mock_open_file.call_count == 10
        assert mock_sleep.call_count == 10

    @patch("builtins.open", side_effect=Exception("Unexpected error"))
    def test_unexpected_error(self, mock_open_file, mock_sleep, tmp_path: Path):
        """
        Test that the function raises a Exception when an unexpected error occurs.
        """
        file_path = tmp_path / "error_file.txt"
        file_path.write_text("Test content")
        with pytest.raises(Exception, match="Unexpected error"):
            utils.verify_file_is_accessible(file_path)
        mock_open_file.assert_called_once_with(file_path, mode="r")
        mock_sleep.assert_not_called()

    @patch(
        "builtins.open",
        side_effect=[PermissionError] * 5 + [mock_open(read_data="data").return_value],
    )
    def test_eventual_accessible_file(self, mock_open_file, mock_sleep, tmp_path: Path):
        """
        Test that the function eventually succeeds after initial PermissionErrors.
        """
        file_path = tmp_path / "eventual_accessible_file.txt"
        file_path.write_text("Test content")
        assert utils.verify_file_is_accessible(file_path) is True
        assert mock_open_file.call_count == 6
        assert mock_sleep.call_count == 5
