from pathlib import Path
from warnings import warn

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTFigure, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument, PDFPasswordIncorrect
from pdfminer.pdfparser import PDFParser

from .utils import adjust_phrases


def load(
    file_path: Path, password: str = None, encoding: str = "utf-8", mode: str = "r"
) -> dict[str, str]:
    """Load a PDF file and extract its text content.

    Args:
        file_path (Path): path to the PDF file.
        password (str, optional): password for encrypted PDF files. Defaults to None.
        encoding (str, optional): encoding type (not implemented). Defaults to "utf-8".
        mode (str, optional): file mode (not implemented). Defaults to 'r'.

    :returns: dictionary with page numbers as keys and extracted text as values.
    :rtype: dict[str, str]
    """
    try:
        with file_path.open("rb") as file:
            parser = PDFParser(file)
            PDFDocument(parser, password=password)
    except PDFPasswordIncorrect:
        warn_msg = f"PDF file {file_path} is encrtyped. Need password!"
        warn(warn_msg)
        return {"Error": warn_msg}
    pages = {}
    for num_page, pagina_layout in enumerate(
        extract_pages(pdf_file=file_path, password=password), start=1
    ):
        page_text = ""
        for element in pagina_layout:
            if isinstance(element, LTTextBoxHorizontal):
                page_text += element.get_text()
            elif isinstance(element, LTFigure):
                pass
        pages[f"Page {num_page}"] = adjust_phrases(page_text)
    return pages


def write(
    file_path: str,
    data: dict[str, str],
    password: str = None,
    encoding: str = "utf-8",
    mode: str = "w",
) -> None:
    """Function to write pdf files.

    Args:
        file_path (str): path to save the pdf file.
        data (dict[str, str]): data to be written in the pdf file.
        password (str, optional): password to encrypt the pdf file. Defaults to None.
        encoding (str, optional): encoding type. Defaults to "utf-8".
        mode (str, optional): file mode. Defaults to 'w'.

    Raises:
        NotImplementedError: function not implemented yet.
    """
    raise NotImplementedError("I can't write pdf files yet!")
