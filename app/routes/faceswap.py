# app/routes/faceswap.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models import UserModel
from app.database.connection import images_collection, users_collection
from app.routes.users import get_current_user
from bson.objectid import ObjectId
import os
import cv2
import numpy as np
import insightface
from insightface.model_zoo import get_model

router = APIRouter()

@router.post("/")
async def face_swap(
    selfie_id: str,
    target_image: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):
    # Ensure the images directory exists
    os.makedirs('images', exist_ok=True)

    # Retrieve the selfie image from the database
    selfie_record = await images_collection.find_one({"_id": ObjectId(selfie_id), "user_id": str(current_user.id)})
    if not selfie_record:
        raise HTTPException(status_code=404, detail="Selfie not found")

    selfie_path = selfie_record["image_url"]
    target_path = f"images/{current_user.id}_{target_image.filename}"

    # Save the uploaded target image
    with open(target_path, "wb") as file_object:
        file_object.write(await target_image.read())

    # Initialize the face swap model
    model = get_model('inswapper_128.onnx', download=True, 
                      providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    model.prepare(ctx_id=0)

    # Read the images
    source_img = cv2.imread(selfie_path)
    target_img = cv2.imread(target_path)

    # Check if images are loaded correctly
    if source_img is None:
        raise HTTPException(status_code=400, detail="Failed to load selfie image.")
    if target_img is None:
        raise HTTPException(status_code=400, detail="Failed to load target image.")

    # Perform face swap
    swapped_img = model.get(target_img, source_img, paste_back=True)

    # Save the swapped image
    output_path = f"images/{current_user.id}_swapped_{target_image.filename}"
    cv2.imwrite(output_path, swapped_img)

    # Update user's balance
    await users_collection.update_one(
        {"_id": current_user.id},
        {"$inc": {"balance": -1.0}}
    )

    return {"swapped_image_url": output_path}