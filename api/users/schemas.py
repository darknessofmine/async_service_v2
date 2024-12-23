from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserResponse(BaseModel):
    username: str
    email: str
