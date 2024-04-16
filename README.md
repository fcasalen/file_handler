# file_handler
project to load and write files that are often used

```python
from file_handler import FileHandler

#loading data from two files in filepath1 and filepath2
data = FileHandler.load(file_paths=['filepath1.txt', 'filepath2.json'])

#writing data to two files in filepath3 and filepath4
FileHandler.write(file_handler_data={
    'filepath3.json': data_for_this_file3,
    'filepath4.json': data_for_this_file4
})
```
