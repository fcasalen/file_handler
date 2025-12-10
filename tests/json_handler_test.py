import json
from datetime import datetime
from pathlib import Path

from src.file_handler import json_handler


def test_json_handler_write(tmp_path: Path):
    test_file = tmp_path / "test.json"
    test_data = {
        "name": "Test",
        "value": 123,
        "timestamp": datetime(2024, 1, 1, 12, 0, 0),
    }
    json_handler.write(file_path=test_file, encoding="utf-8", data=test_data)
    assert test_file.exists()
    with open(test_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == {
        "name": "Test",
        "value": 123,
        "timestamp": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }


def test_json_handler_load(tmp_path: Path):
    test_file = tmp_path / "test.json"
    test_data = {
        "name": "Test",
        "value": 123,
        "timestamp": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)
    loaded_data = json_handler.load(test_file)
    assert loaded_data == {
        "name": "Test",
        "value": 123,
        "timestamp": datetime(2024, 1, 1, 12, 0, 0),
    }


def test_round_trip(tmp_path: Path):
    test_file = tmp_path / "test.json"
    original_data = {
        "name": "IntegrationTest",
        "value": 456,
        "timestamp": datetime(2024, 6, 15, 15, 30, 0),
    }
    json_handler.write(file_path=test_file, encoding="utf-8", data=original_data)
    loaded_data = json_handler.load(test_file)
    assert loaded_data == original_data
