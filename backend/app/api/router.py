from fastapi import APIRouter

from app.api.endpoints import auth, interfaces

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(interfaces.router, prefix="/interfaces", tags=["接口管理"])
