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
    is_verified: bool


class UserLogin(BaseModel):
    username: str
    password: str


class UserPasswordReset(BaseModel):
    new_password: str
    new_password_repeat: str


class UserUpdate(BaseModel):
    email: EmailStr
