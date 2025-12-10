import json
from pathlib import Path

import pytest

from src.file_handler import ppt_handler


def test_ppt_handler_load():
    this_dir = Path(__file__).parent
    slide_data = ppt_handler.load(
        file_path=this_dir / "mocks" / "Dickinson_Sample_Slides.pptx", encoding="utf-8"
    )
    with open(
        this_dir / "mocks" / "Dickinson_Sample_Slides_extracted.json",
        "r",
        encoding="utf-8",
    ) as f:
        expected_data = json.load(f)
    assert slide_data == expected_data


def test_ppt_handler_write(tmp_path: Path):
    with pytest.raises(NotImplementedError, match="I can't write ppt files yet!"):
        ppt_handler.write(file_path=tmp_path / "output.pptx", data="", encoding="utf-8")


def test_round_trip(tmp_path: Path):
    this_dir = Path(__file__).parent
    with open(
        this_dir / "mocks" / "Dickinson_Sample_Slides_extracted.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes(
        (this_dir / "mocks" / "Dickinson_Sample_Slides.pptx").read_bytes()
    )
    with pytest.raises(NotImplementedError, match="I can't write ppt files yet!"):
        ppt_handler.write(file_path=file_path, data="", encoding="utf-8")
    slide_data = ppt_handler.load(file_path)
    assert slide_data == data
