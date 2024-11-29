from fastapi import FastAPI

app = FastAPI()

# Import routers
from app.routes.users import router as users_router
from app.routes.images import router as images_router
from app.routes.faceswap import router as faceswap_router

# Include routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(images_router, prefix="/images", tags=["Images"])
app.include_router(faceswap_router, prefix="/faceswap", tags=["FaceSwap"])
