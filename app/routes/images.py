# app/routes/images.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models import UserModel, ImageModel
from app.database.connection import images_collection
from app.routes.users import get_current_user
from typing import List
import os

router = APIRouter()

@router.post("/upload_selfie")
async def upload_selfie(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):
    file_location = f"images/{current_user.id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    image_record = {
        "user_id": str(current_user.id),
        "image_url": file_location
    }
    await images_collection.insert_one(image_record)
    return {"info": "Selfie uploaded successfully"}

@router.get("/{user_id}/images", response_model=List[ImageModel])
async def get_user_images(user_id: str):
    images = images_collection.find({"user_id": user_id})
    return [ImageModel(**img) async for img in images]
