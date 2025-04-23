import os
from datetime import datetime
from typing import (
    List,
    Optional,
)

from fastapi.responses import StreamingResponse
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)
from typing_extensions import Self

# from responses import delete

# from files_api.s3.delete_objects import delete_s3_object
# from files_api.s3.read_objects import (
#     fetch_s3_object,
#     fetch_s3_objects_metadata,
#     fetch_s3_objects_using_page_token,
#     object_exists_in_s3,
# )
# from files_api.s3.write_objects import upload_s3_object

# constants
DEFAULT_GET_FILES_PAGE_SIZE = 10
DEFAULT_GET_FILES_MAX_PAGE_SIZE = 100
DEFAULT_GET_FILES_MIN_PAGE_SIZE = 10
DEFAULT_GET_FILES_DIRECTORY = ""

####################################
# --- Request/response schemas --- #
####################################


# read (cRud)
class FileMetadata(BaseModel):
    file_path: str
    last_modified: datetime
    size_bytes: int

# read (cRud)
class GetFilesResponse(BaseModel):
    files: List[FileMetadata]
    next_page_token: Optional[str]
 
# read (cRud)   
class GetFilesQueryParams(BaseModel):
    page_size: int = Field(
        default=DEFAULT_GET_FILES_PAGE_SIZE, 
        ge=DEFAULT_GET_FILES_MIN_PAGE_SIZE, 
        le=DEFAULT_GET_FILES_MAX_PAGE_SIZE)
    
    directory: Optional[str] = DEFAULT_GET_FILES_DIRECTORY
    page_token: Optional[str] = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.page_token: #if page token is set, then page size and directory should not be set
            get_files_query_params: dict = self.model_dump(exclude_unset=True)
            page_size_set ="page_size" in get_files_query_params.keys()
            directory_set = "directory" in get_files_query_params.keys()
            if page_size_set or directory_set:
                raise ValueError("page_token is mutually exclusive with page_size and directory")
        return self

# delete (cruD)
class DeleteFileResponse(BaseModel):
    message: str
    
# create.update (Crud)
# why do we need to define this class?
# because we need to return a response with the file path and message
# when we upload a file
class PutFileResponse(BaseModel):
    file_path: str
    message: str