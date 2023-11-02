from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db.database import get_db
from fastapi_service.models import User
from fastapi_service.token import create_access_token
from module.hashing import get_password_hash, verify_password
from sqlalchemy.orm import Session

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI, HTTPException, status, Depends
from fastapi_service.models import SignupRequest, SignupResponse
from module.hashing import get_password_hash
from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import Session
from routers import authentication
from fastapi_service.oauth2 import get_current_user

router = APIRouter(tags=["dummy"])


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(current_user: User = Depends(get_current_user)):
    return {"msg": "pong"}
