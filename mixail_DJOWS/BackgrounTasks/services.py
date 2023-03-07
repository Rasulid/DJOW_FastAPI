from datetime import datetime

import aiofiles
import shutil
from fastapi import UploadFile, BackgroundTasks, HTTPException
from uuid import uuid4
import datetime
from models import Video, User


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: str,
        background_tasks: BackgroundTasks
):
    file_name = f"static/images/{user.id}_{uuid4()}.mp4"
    if file.content_type == "video/mp4":
        background_tasks.add_task(write_video, file_name, file)

    else:
        raise HTTPException(status_code=418, detail="It's not a mp4")

    return await Video.objects.create(file=file.filename, user=user,
                                      title=title, description=description,
                                      create_at=datetime.datetime.now())


def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(filename, 'wb') as buffer:
    #     data = await file.read()
    #     await buffer.write(data)

    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
