from fastapi import APIRouter, File, Form, UploadFile, BackgroundTasks, HTTPException, Request
from typing import List
from models import Video, User
from schemas import UploadVideo, GetVideo, GetListVideo
from services import save_video, open_file
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


@router.get("/video/{video_pk}")
async def get_video(video_id: int):
    file = await Video.objects.select_related("user").get(pk=video_id)
    file_lake = open(file.file, mode="rb")
    return StreamingResponse(file_lake, media_type="video/mp4")


@router.get("/user/{user_id}", response_model=List[GetListVideo])
async def get_list_video(user_id: int):
    video_list = await Video.objects.filter(user=user_id).all()
    return video_list


@router.get("/video/{video_id}")
async def get_streaming_video(request: Request, video_id: int) -> StreamingResponse:
    file, status_code, content_lenght, headers = await open_file(request, video_id)
    print("file", file)

    response = StreamingResponse(
        file,
        media_type="video/mp4",
        status_code=status_code,
    )

    response.headers.update({
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_lenght),
        **headers,
    })
    return response
