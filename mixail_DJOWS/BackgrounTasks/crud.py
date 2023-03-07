from fastapi import APIRouter, File, Form, UploadFile, BackgroundTasks, HTTPException
from typing import List
from models import Video, User
from schemas import UploadVideo, GetVideo
from services import save_video
from fastapi.responses import StreamingResponse
from uuid import uuid4

router = APIRouter(tags=['UploadFile'])


@router.post("/")
async def crate_video(background_tasks: BackgroundTasks,
                      title: str = Form(...),
                      description: str = Form(...),
                      file: UploadFile = File(...)):
    user = await User.objects.first()
    print(user)
    return await save_video(user=user, file=file, title=title,
                            description=description, background_tasks=background_tasks)


@router.get("/video/{video_id}", response_model=GetVideo)
async def test(video_id: int):
    """
    С select_related("user") этим мы хотим сказать что ба он вывел все информации о данным
    и он подтянет всё косаюший этой данной

    """
    file = await Video.objects.select_related("user").get(pk=video_id)
    file_lake = open(f'static/images/{file.dict().get("file")}', mode="rb")
    return StreamingResponse(file_lake, media_type="video/mp4")
