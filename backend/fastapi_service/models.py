# fastapi_service/models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from db.database import Base


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    fullname = Column(String, index=True)
    password = Column(String)


class SignupRequest(BaseModel):
    username: str
    fullname: str
    password: str


class SignupResponse(BaseModel):
    username: str
    fullname: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str  # Adjusted to use username


class Question(BaseModel):
    question: str
    pdfs: list[str]
