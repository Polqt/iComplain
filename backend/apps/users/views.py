
from ninja import Router
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest
from .schemas import SignupRequest, LoginRequest, UserResponse, AuthResponse

User = get_user_model()
router = Router(tags=["User"])

@router.post("/register", response=AuthResponse)
def register(request: HttpRequest, data: SignupRequest):
    if User.objects.filter(email=data.email).exists():
        return AuthResponse(success=False, message="Email already registered.", user=None)

    user = User.objects.create_user(
        email=data.email,
        password=data.password
    )
    return AuthResponse(
        success=True,
        message="Student account created successfully.",
        user=UserResponse(id=user.id, email=user.email)
    )


@router.post("/login", response=AuthResponse)
def login_user(request: HttpRequest, data: LoginRequest):
    user = authenticate(
        request,
        email=data.email,
        password=data.password
    )
    if not user:
        return AuthResponse(
            success=False,
            message="Invalid username or password.",
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
    logout(request)
    return AuthResponse(
        success=True,
        message="Logged out successfully.",
        user=None
    )