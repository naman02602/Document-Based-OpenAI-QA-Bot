from fastapi import APIRouter, Depends, status
from fastapi_service.models import User
from fastapi import status, Depends
from fastapi_service.oauth2 import get_current_user

router = APIRouter(tags=["dummy"])


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(current_user: User = Depends(get_current_user)):
    return {"msg": "pong"}
