from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

class UploadVideo(BaseModel):
    title: str
    description: str
    filename: List[str] = None



class GetVideo(BaseModel):
    user: List[User]
    video: List[UploadVideo]


class Massages(BaseModel):
    massages: str