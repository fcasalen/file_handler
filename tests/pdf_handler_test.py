import json
from pathlib import Path
from unittest.mock import patch

import pytest
from pdfminer.pdfdocument import PDFPasswordIncorrect

from src.file_handler import pdf_handler


def test_pdf_handler_load():
    this_dir = Path(__file__).parent
    pdf_data = pdf_handler.load(this_dir / "mocks" / "somatosensory.pdf")
    with open(
        this_dir / "mocks" / "somatosensory_extracted.json", "r", encoding="utf-8"
    ) as f:
        expected_data = json.load(f)
    assert pdf_data == expected_data


def test_pdf_handler_write(tmp_path: Path):
    with pytest.raises(NotImplementedError, match="I can't write pdf files yet!"):
        pdf_handler.write(
            file_path=tmp_path / "output.pdf", encoding="utf-8", data="", mode="w"
        )


def test_round_trip(tmp_path: Path):
    this_dir = Path(__file__).parent
    with open(
        this_dir / "mocks" / "somatosensory_extracted.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes((this_dir / "mocks" / "somatosensory.pdf").read_bytes())
    with pytest.raises(NotImplementedError, match="I can't write pdf files yet!"):
        pdf_handler.write(file_path=file_path, encoding="utf-8", data=data, mode="w")
    pdf_data = pdf_handler.load(file_path)
    assert pdf_data == data


def test_pdf_handler_load_encrypted(tmp_path: Path):
    this_dir = Path(__file__).parent
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes((this_dir / "mocks" / "somatosensory.pdf").read_bytes())
    with patch(
        "src.file_handler.pdf_handler.PDFDocument", side_effect=PDFPasswordIncorrect
    ):
        result = pdf_handler.load(file_path)
        assert result == {"Error": f"PDF file {file_path} is encrtyped. Need password!"}
