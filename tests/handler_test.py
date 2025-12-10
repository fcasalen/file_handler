import json
import re
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.file_handler.handler import FileHandler


class TestCSV:
    def test_csv_round_trip_single_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.csv"
        write_result = FileHandler.write(file_handler_data={file_path: df})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        pd.testing.assert_frame_equal(loaded[str(file_path)], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.csv_handler.write") as mock_write,
            patch("src.file_handler.handler.csv_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: df})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_csv_round_trip_multi_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.csv"
        write_result = FileHandler.write(
            file_handler_data={file_path: df}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        pd.testing.assert_frame_equal(loaded[str(file_path)], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}


class TestExcel:
    def test_excel_round_trip_single_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.xlsx"
        write_result = FileHandler.write(file_handler_data={file_path: df})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        pd.testing.assert_frame_equal(loaded[str(file_path)]["Sheet1"], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert list(loaded[str(file_path)].keys()) == ["Sheet1"]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.excel_handler.write") as mock_write,
            patch("src.file_handler.handler.excel_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: df})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_excel_round_trip_multi_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.xlsx"
        write_result = FileHandler.write(
            file_handler_data={file_path: df}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        pd.testing.assert_frame_equal(loaded[str(file_path)]["Sheet1"], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert list(loaded[str(file_path)].keys()) == ["Sheet1"]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}


class TestJSON:
    def test_json_round_trip_single_process(self, tmp_path: Path):
        data = {"test_key": 2, "list_key": [1, 2, 3]}
        file_path = tmp_path / "test.json"
        write_result = FileHandler.write(file_handler_data={file_path: data})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.json_handler.write") as mock_write,
            patch("src.file_handler.handler.json_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: data})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_json_round_trip_multi_process(self, tmp_path: Path):
        data = {"test_key": 2, "list_key": [1, 2, 3]}
        file_path = tmp_path / "test.json"
        write_result = FileHandler.write(
            file_handler_data={file_path: data}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}


class TestParquet:
    def test_parquet_round_trip_single_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.parquet"
        write_result = FileHandler.write(file_handler_data={file_path: df})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        pd.testing.assert_frame_equal(loaded[str(file_path)], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.parquet_handler.write") as mock_write,
            patch("src.file_handler.handler.parquet_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: df})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_parquet_round_trip_multi_process(self, tmp_path: Path):
        df = pd.DataFrame({"M": [1, 2], "N": [3, None]}).convert_dtypes()
        file_path = tmp_path / "df.parquet"
        write_result = FileHandler.write(
            file_handler_data={file_path: df}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        pd.testing.assert_frame_equal(loaded[str(file_path)], df)
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}


class TestPDF:
    def test_pdf_round_trip_single_process(self, tmp_path: Path):
        this_dir = Path(__file__).parent
        with open(
            this_dir / "mocks" / "somatosensory_extracted.json", "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
        file_path = tmp_path / "test.pdf"
        file_path.write_bytes((this_dir / "mocks" / "somatosensory.pdf").read_bytes())
        write_result = FileHandler.write(file_handler_data={file_path: data})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write pdf files yet!"
        }
        assert write_again == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write pdf files yet!"
        }
        with (
            patch("src.file_handler.handler.pdf_handler.write") as mock_write,
            patch("src.file_handler.handler.pdf_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: data})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_pdf_round_trip_multi_process(self, tmp_path: Path):
        this_dir = Path(__file__).parent
        with open(
            this_dir / "mocks" / "somatosensory_extracted.json", "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
        file_path = tmp_path / "test.pdf"
        file_path.write_bytes((this_dir / "mocks" / "somatosensory.pdf").read_bytes())
        write_result = FileHandler.write(
            file_handler_data={file_path: data}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write pdf files yet!"
        }
        assert write_again == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write pdf files yet!"
        }


class TestPPT:
    def test_ppt_round_trip_single_process(self, tmp_path: Path):
        this_dir = Path(__file__).parent
        with open(
            this_dir / "mocks" / "Dickinson_Sample_Slides_extracted.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)
        file_path = tmp_path / "Dickinson_Sample_Slides.pptx"
        file_path.write_bytes(
            (this_dir / "mocks" / "Dickinson_Sample_Slides.pptx").read_bytes()
        )
        write_result = FileHandler.write(file_handler_data={file_path: data})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write ppt files yet!"
        }
        assert write_again == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write ppt files yet!"
        }
        with (
            patch("src.file_handler.handler.ppt_handler.write") as mock_write,
            patch("src.file_handler.handler.ppt_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: data})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_ppt_round_trip_multi_process(self, tmp_path: Path):
        this_dir = Path(__file__).parent
        with open(
            this_dir / "mocks" / "Dickinson_Sample_Slides_extracted.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)
        file_path = tmp_path / "Dickinson_Sample_Slides.pptx"
        file_path.write_bytes(
            (this_dir / "mocks" / "Dickinson_Sample_Slides.pptx").read_bytes()
        )
        write_result = FileHandler.write(
            file_handler_data={file_path: data}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write ppt files yet!"
        }
        assert write_again == {
            str(
                file_path
            ): f"Error writing file {str(file_path)}: I can't write ppt files yet!"
        }


class TestTXT:
    def test_txt_round_trip_single_process(self, tmp_path: Path):
        data = "oi"
        file_path = tmp_path / "test.txt"
        write_result = FileHandler.write(file_handler_data={file_path: data})
        loaded = FileHandler.load(file_path)
        write_again = FileHandler.write(file_handler_data=loaded)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.txt_handler.write") as mock_write,
            patch("src.file_handler.handler.txt_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: data})
            FileHandler.load(file_path)
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_txt_round_trip_multi_process(self, tmp_path: Path):
        data = "oi"
        file_path = tmp_path / "test.txt"
        write_result = FileHandler.write(
            file_handler_data={file_path: data}, multiprocess=True
        )
        loaded = FileHandler.load(file_path, multiprocess=True)
        write_again = FileHandler.write(file_handler_data=loaded, multiprocess=True)
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}

    def test_txt_round_trip_single_process_mode_rb(self, tmp_path: Path):
        data = b"oi"
        file_path = tmp_path / "test.xlsx"
        write_result = FileHandler.write(file_handler_data={file_path: data}, mode="wb")
        loaded = FileHandler.load(file_path, mode="rb")
        write_again = FileHandler.write(file_handler_data=loaded, mode="wb")
        assert loaded[str(file_path)] == data
        assert list(loaded.keys()) == [str(file_path)]
        assert write_result == {str(file_path): True}
        assert write_again == {str(file_path): True}
        with (
            patch("src.file_handler.handler.txt_handler.write") as mock_write,
            patch("src.file_handler.handler.txt_handler.load") as mock_load,
        ):
            FileHandler.write(file_handler_data={file_path: data}, mode="wb")
            FileHandler.load(file_path, mode="rb")
            mock_write.assert_called_once()
            mock_load.assert_called_once()

    def test_txt_error_loading(self, tmp_path: Path):
        file_path = tmp_path / "non_existent.xlsx"
        file_path.write_text("")
        result = FileHandler.load(file_path)
        assert result == {
            str(
                file_path
            ): f"Error loading file {str(file_path)}: Excel file format cannot be "
            f"determined, you must specify an engine manually."
        }

    def test_txt_round_trip_multiple_files_as_list(self, tmp_path: Path):
        data1 = "oi"
        data2 = "hello"
        file_path1 = tmp_path / "test1.txt"
        file_path2 = tmp_path / "test2.txt"
        FileHandler.write(file_handler_data={file_path1: data1, file_path2: data2})
        loaded = FileHandler.load([str(file_path1), str(file_path2)])
        assert loaded[str(file_path1)] == data1
        assert loaded[str(file_path2)] == data2

    def test_txt_round_trip_multiple_files_as_dict(self, tmp_path: Path):
        data1 = "oi"
        data2 = "hello"
        file_path1 = tmp_path / "test1.txt"
        file_path2 = tmp_path / "test2.txt"
        FileHandler.write(file_handler_data={file_path1: data1, file_path2: data2})
        loaded = FileHandler.load({str(file_path1): None, str(file_path2): None})
        assert loaded[str(file_path1)] == data1
        assert loaded[str(file_path2)] == data2

    def test_txt_invalid_file_path(self):
        with pytest.raises(
            AssertionError,
            match=re.escape("file_paths should be str, list[str] or dict[str, str]"),
        ):
            FileHandler.load(1)

    def test_txt_file_path_dont_exist(self, tmp_path: Path):
        file_path1 = tmp_path / "test1.txt"
        file_path2 = tmp_path / "test2.txt"
        with pytest.raises(
            AssertionError, match=re.escape("all file paths should exist")
        ):
            FileHandler.load({str(file_path1): None, str(file_path2): None})

    def test_txt_invalid_password_type(self, tmp_path: Path):
        file_path1 = tmp_path / "test1.txt"
        file_path1.write_text("oi")
        with pytest.raises(
            AssertionError, match=re.escape("password values should be str or None")
        ):
            FileHandler.load({str(file_path1): 123})

    def test_txt_invalid_file_handler_data_type(self):
        with pytest.raises(
            AssertionError,
            match=re.escape(
                "file_handler_data should be a dict[str, str | bytes | list | "
                "pd.DataFrame | dict[str, str | pd.DataFrame | Any]]"
            ),
        ):
            FileHandler.write(file_handler_data=["invalid"])

    def test_txt_invalid_file_handler_data_key_type(self):
        with pytest.raises(
            AssertionError,
            match="all keys in file_handler_data should be str representing file paths",
        ):
            FileHandler.write(file_handler_data={123: "data"})

    def test_file_inacessible(self, tmp_path: Path):
        file_path = tmp_path / "inacessible_file.txt"
        with patch(
            "src.file_handler.handler.utils.verify_file_is_accessible",
            return_value=False,
        ):
            result = FileHandler.write(file_handler_data={file_path: "data"})
            assert result == {
                str(file_path): f"File {str(file_path)} is not accessible for writing."
            }
