from pydantic import BaseModel, field_validator, ConfigDict
from os.path import exists, dirname
from os import makedirs
from pandas import DataFrame

class StringData(BaseModel):
    data:str

class TxtData(BaseModel):
    data:dict[str, str]

class JsonData(BaseModel):
    data:dict[str, list|dict|str]

class FilePaths(BaseModel):
    file_paths:list[str]

    @field_validator("file_paths")
    def validate_file_exists(cls, value):
        invalid_file_paths = [v for v in value if not exists(v)]
        if invalid_file_paths:
            raise ValueError(f"Files {', '.join(invalid_file_paths)} doesn't not exist.")

class FileHanderData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data:dict[str, dict[str, str|list|DataFrame]]

    @field_validator("data")
    def validate_file_exists(cls, value):
        for k in value.keys():
            dir_name = dirname(k)
            if not exists(dir_name):
                makedirs(dir_name)

class DataFrameData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data:dict[str, DataFrame]