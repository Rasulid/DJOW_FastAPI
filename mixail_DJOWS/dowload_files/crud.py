from fastapi import APIRouter, File, UploadFile
import shutil
from typing import List


router = APIRouter()

@router.post("/root")
async def root(file: List[UploadFile] = File(...)):
    result = []
    for image in file:
        with open(f'static/images/{image.filename}',"wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            result.append(image.filename)

    return {"filename": result}