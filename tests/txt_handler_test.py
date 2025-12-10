from pathlib import Path

from src.file_handler import txt_handler


def test_load_string(tmp_path: Path):
    data = "This is a test file.\nWith multiple lines.\nEnd of file."
    file_path = tmp_path / "txt_handler_test.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    loaded_data = txt_handler.load(file_path)
    assert loaded_data == data


def test_load_bytes(tmp_path: Path):
    data = b"This is a test file.\nWith multiple lines.\nEnd of file."
    file_path = tmp_path / "txt_handler_test.bin"
    with open(file_path, "wb") as f:
        f.write(data)
    loaded_data = txt_handler.load(file_path, mode="rb", encoding=None)
    assert loaded_data == data


def test_write_string(tmp_path: Path):
    data = "This is a test file.\nWith multiple lines.\nEnd of file."
    file_path = tmp_path / "txt_handler_write_test.txt"
    txt_handler.write(file_path, data)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = f.read()
    assert loaded_data == data


def test_write_bytes(tmp_path: Path):
    data = b"This is a test file.\nWith multiple lines.\nEnd of file."
    file_path = tmp_path / "txt_handler_write_test.bin"
    txt_handler.write(file_path, data, mode="wb", encoding=None)
    with open(file_path, "rb") as f:
        loaded_data = f.read()
    assert loaded_data == data


def test_round_trip_string(tmp_path: Path):
    data = "Round trip test data.\nAnother line."
    file_path = tmp_path / "txt_handler_round_trip.txt"
    txt_handler.write(file_path, data)
    loaded_data = txt_handler.load(file_path)
    assert loaded_data == data


def test_round_trip_bytes(tmp_path: Path):
    data = b"Round trip test data.\nAnother line."
    file_path = tmp_path / "txt_handler_round_trip.bin"
    txt_handler.write(file_path, data, mode="wb", encoding=None)
    loaded_data = txt_handler.load(file_path, mode="rb", encoding=None)
    assert loaded_data == data
