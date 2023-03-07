import datetime
from fastapi import APIRouter, File, Form, UploadFile
import shutil
from typing import List
from models import Video, User
from schemas import UploadVideo, GetVideo

router = APIRouter(tags=['UploadFile'])


@router.post("/")
async def crate_video(title: str = Form(...),
                      description: str = Form(...),
                      file: UploadFile = File(...)):
    with open(f'static/images/{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user_ = await User.objects.first()
    print(user_)
    return await Video.objects.create(file=file.filename, user=user_,
                                      title=title, description=description,
                                      create_at=datetime.datetime.now())


@router.get("/video/{video_id}", response_model=GetVideo)
async def test(video_id: int):
    """
    С select_related("user") этим мы хотим сказать что ба он вывел все информации о данным
    и он подтянет всё косаюший этой данной

    """
    return await Video.objects.select_related("user").get(pk=video_id)
