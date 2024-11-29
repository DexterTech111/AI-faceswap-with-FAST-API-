# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import UserModel, UserCreateModel, UserPublicModel
from app.database.connection import users_collection
from app.utils.auth import generate_api_key, generate_api_token
from bson.objectid import ObjectId
from typing import List, Optional

router = APIRouter()

async def get_current_user(api_key: str, api_token: str):
    user = await users_collection.find_one({"api_key": api_key, "api_token": api_token})
    if user and user["is_active"]:
        return UserModel(**user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

async def admin_required(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@router.post("/", response_model=UserModel)
async def create_user(user: UserCreateModel, is_admin: Optional[bool] = False):
    api_key = generate_api_key()
    api_token = generate_api_token()
    user_dict = user.model_dump()
    user_dict.update({
        "api_key": api_key,
        "api_token": api_token,
        "balance": 0.0,
        "is_active": True,
        "is_admin": is_admin
    })
    new_user = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return UserModel(**created_user)

@router.get("/", response_model=List[UserPublicModel])
async def get_all_users(admin_user: UserModel = Depends(admin_required)):
    users = []
    async for user in users_collection.find():
        users.append(UserPublicModel(**user))
    return users

@router.get("/{user_id}", response_model=UserPublicModel)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserPublicModel(**user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put("/{user_id}/status")
async def update_user_status(user_id: str, is_active: bool):
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": is_active}}
    )
    if result.modified_count == 1:
        return {"message": "User status updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/{user_id}/balance")
async def get_balance(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"balance": user["balance"]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
