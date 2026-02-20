from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

class LoginRequest(BaseModel):
    email: str
    password: str


class GoogleLoginRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool = True
    role: Literal["student", "admin"]
    name: str | None = None
    avatar: str | None = None

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: UserResponse | None = None
