from pydantic import BaseModel

class InitializeDBRequest(BaseModel):
    user_name: str

class ImageRequest(BaseModel):
    image_path: str

class FolderRequest(BaseModel):
    folder_path: str

class ImageSearch(BaseModel):
    query: str
