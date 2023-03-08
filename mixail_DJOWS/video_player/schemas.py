from typing import List, Optional
from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str
    create_at: datetime.datetime


class GetListVideo(BaseModel):
    id: int
    title: str
    description: str


class GetVideo(GetListVideo):
    user: User



