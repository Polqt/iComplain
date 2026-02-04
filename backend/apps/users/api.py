from ninja import Router
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest
from pydantic import BaseModel, EmailStr, field_validator

User = get_user_model()
router = Router(tags=["User"])


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
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: UserResponse | None = None


#Routes
@router.get("/ping")
def ping(request):
    return {"message": "users api working"}


@router.post("/register", response=AuthResponse)
def register(request: HttpRequest, data: SignupRequest):
    """Register a new student account with email and password"""
    
    # Check if email already exists
    if User.objects.filter(email=data.email).exists():
        return AuthResponse(
            success=False,
            message="Email already registered.",
            user=None
        )
    
    # Create user
    user = User.objects.create_user(
        email=data.email,
        password=data.password
    )

    return AuthResponse(
        success=True,
        message="Student account created successfully.",
        user=UserResponse(id=user.id, email=user.email, is_active=user.is_active)
    )


@router.post("/login", response=AuthResponse)
def login_user(request: HttpRequest, data: LoginRequest):
    """Login with email and password"""
    
    user = authenticate(
        request,
        email=data.email,
        password=data.password
    )

    if not user:
        return AuthResponse(
            success=False,
            message="Invalid email or password.",
            user=None
        )
    
    login(request, user)
    return AuthResponse(
        success=True,
        message="Logged in successfully.",
        user=UserResponse(id=user.id, email=user.email, is_active=user.is_active)
    )


@router.post("/logout", response=AuthResponse)
def logout_user(request: HttpRequest):
    """Logout the current user"""
    logout(request)
    return AuthResponse(
        success=True,
        message="Logged out successfully.",
        user=None
    )