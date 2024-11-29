# app/database/connection.py
import motor.motor_asyncio
from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DETAILS)
database = client.faceswap_db

users_collection = database.get_collection("users")
images_collection = database.get_collection("images")
