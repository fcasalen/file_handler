# File Handler

A Python package for handling multiple file formats with a unified interface. Simplify your file operations with support for CSV, Excel, JSON, PDF, PowerPoint, Parquet, and text files.

## Features

- **Multi-format support**: CSV, Excel (.xlsx), JSON, PDF, PowerPoint (.ppt/.pptx), Parquet, and text files (other files types will be treated as plain text). Can work with bytes files as well (just use a mode with 'b').
- **Unified API**: Single interface for all file operations
- **Batch processing**: Load/write multiple files at once
- **Password protection**: Support for password-protected PDFs and Excel files
- **Performance optimization**: Optional multiprocessing for large file operations
- **Progress tracking**: Built-in progress bars for batch operations
- **Type safety**: Full type hints and validation

## Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/fcasalen/file_handler.git
cd file_handler
pip install .
```

## Quick Start

### Basic Usage

```python
from file_handler import FileHandler

# Load a single file
data = FileHandler.load(file_paths='data.csv')

# Load multiple files
data = FileHandler.load(file_paths=['data.csv', 'config.json', 'report.xlsx'])

# Write data to a file
FileHandler.write(file_handler_data={
    'output.json': {'key': 'value'},
    'results.csv': dataframe
})
```

### Advanced Usage

```python
# Load password-protected files
data = FileHandler.load(
    file_paths={'protected.pdf': 'password123', 'normal.txt': None}
)

# Batch processing with multiprocessing
data = FileHandler.load(
    file_paths=['file1.csv', 'file2.csv', 'file3.csv'],
    multiprocess=True,
    progress_bar=True
)

# Custom encoding and mode
FileHandler.write(
    file_handler_data={'output.txt': 'Hello World'},
    encoding='utf-8',
    mode='w'
)
```

## Supported File Formats

|   Format   |    Extension    | Read | Write | Password Support |
|------------|-----------------|------|-------|------------------|
| CSV        | `.csv`          |  ✅  |  ✅  |        ❌        |
| Excel      | `.xlsx`, `.xls` |  ✅  |  ✅  |        ❌        |
| JSON       | `.json`         |  ✅  |  ✅  |        ❌        |
| PDF        | `.pdf`          |  ✅  |  ❌* |        ✅        |
| PowerPoint | `.ppt`, `.pptx` |  ✅  |  ❌* |        ❌        |
| Parquet    | `.parquet`      |  ✅  |  ✅  |        ❌        |
| Text       | `all other`     |  ✅  |  ✅  |        ❌        |

*Write functionality not yet implemented for PDF and PowerPoint files.

## API Reference

### FileHandler.load()

Load data from one or multiple files.

**Parameters:**
- `file_paths` (str | list | dict): File path(s) to load
- `encoding` (str, optional): File encoding. Default: 'utf-8'
- `mode` (str, optional): File mode. Default: 'r'
- `progress_bar` (bool, optional): Show progress bar. Default: True
- `multiprocess` (bool, optional): Use multiprocessing. Default: False

**Returns:**
- `dict[str, Any]`

### FileHandler.write()

Write data to one or multiple files.

**Parameters:**
- `file_handler_data` (dict): Dictionary with file paths as keys and data as values
- `encoding` (str, optional): File encoding. Default: 'utf-8'
- `mode` (str, optional): File mode. Default: 'w'
- `progress_bar` (bool, optional): Show progress bar. Default: True
- `multiprocess` (bool, optional): Use multiprocessing. Default: False

**Returns:**
- `dict[str, bool | str]`: Success status or error message for each file

## Examples

### Working with Different File Types

```python
import pandas as pd
from file_handler import FileHandler

# CSV files return pandas DataFrames
csv_data = FileHandler.load(file_paths='data.csv')
print(type(csv_data['data.csv']))  # <class 'pandas.core.frame.DataFrame'>

# JSON files return dictionaries or lists
json_data = FileHandler.load(file_paths='config.json')
print(type(json_data['config.json']))  # <class 'dict'> or <class 'list'>

# Excel files return DataFrames or dict of DataFrames (multi-sheet)
excel_data = FileHandler.load(file_paths='workbook.xlsx')
print(type(excel_data['workbook.xlsx']))  #<class 'dict'> with sheet names as keys

# PDF files return extracted text
pdf_text = FileHandler.load(file_paths='document.pdf')
print(type(pdf_text['document.pdf']))  # <class 'str'>
```

### Batch Processing

```python
# Load multiple files of different types
files = {
    'sales.csv': None,
    'config.json': None,
    'report.pdf': 'secret123'  # password-protected
}

data = FileHandler.load(file_paths=files, multiprocess=True)

# Process results
for file_path, content in data.items():
    print(f"Loaded {file_path}: {type(content)}")
```

### Error Handling

```python
# The package handles errors gracefully
result = FileHandler.load(file_paths=['valid.csv', 'missing.txt'])

# Check for errors in results
for file_path, content in result.items():
    if isinstance(content, str) and content.startswith("Error loading"):
        print(f"Failed to load {file_path}: {content}")
    else:
        print(f"Successfully loaded {file_path}")
```

## Requirements

- Python ≥ 3.11
- pandas
- pdfminer.six
- python-pptx
- openpyxl
- pyarrow
- fastparquet
- pydantic
- loguru
- tqdm
- multiprocess

## Development

### Running Tests

```bash
pytest tests/
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=src/file_handler --cov-report=html
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

**Fernando Casale Neto** - fcasalen@gmail.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
