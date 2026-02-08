from pydantic import BaseModel, EmailStr, field_validator

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('email')
    def validate_usls_email(cls, v):
        if not v.endswith('@usls.edu.ph'):
            raise ValueError('Email must be a valid USLS email address (@usls.edu.ph)')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class LoginRequest(BaseModel):
    email: str
    password: str


class GoogleLoginRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: UserResponse | None = None
