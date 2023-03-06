from fastapi import APIRouter, File, Form, Request, UploadFile
import shutil
from typing import List

from models import Video
from schemas import UploadVideo, GetVideo, Massages
from fastapi.responses import JSONResponse

router = APIRouter(tags=['UploadFile'])


@router.post("/root")
async def root(title: str = Form(...),
               description: str = Form(...),
               file: List[UploadFile] = File(...)):
    result = []
    for image in file:
        with open(f'static/images/{image.filename}', "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            result.append(image.filename)

    return UploadVideo(title=title, description=description, filename=result)


@router.post("/video")
async def post_video(video: Video):
    await video.save()
    return video


@router.get("/infos", response_model=GetVideo, status_code=201)
async def get_video():
    user = [{"id": 12, "username": "root"}]
    video = [{'title': 'Test', 'description': "Description", "filename":
        ["imeges", "filename"]}]
    info = GetVideo(user=user, video=video)
    return info


@router.get("/infos/v2", response_model=GetVideo,
            responses={404: {"model": Massages}})  # if remove responses cade is works
async def get_video_with_responses():
    user = [{"id": 12, "username": "root"}]
    video = [{'title': 'Test', 'description': "Description", "filename":
        ["imeges", "filename"]}]
    info = GetVideo(user=user, video=video)
    return JSONResponse(status_code=404, content={"message": "Item nor Found"})


@router.get("/test")
async def test(req: Request):
    print(req.base_url)
    return {"base_url": req.base_url}
