import datetime
from typing import Optional, Dict, Union
from ormar import Model, Integer, String, ModelMeta, ForeignKey, DateTime
from db import database, metadata

date = datetime.datetime.now()


class MainMeta(ModelMeta):
    database = database
    metadata = metadata


class User(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    username: str = String(max_length=100)


class Video(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    title: str = String(max_length=100)
    description: str = String(max_length=500)
    file: str = String(max_length=1000)
    create_at: datetime.datetime = DateTime(default=datetime.datetime.now, timezone=True)
    user: Optional[Union[User, Dict]] = ForeignKey(User)
