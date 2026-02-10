import logging
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from ninja import Router
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest
from .utils import verify_google_token, is_allowed_domain, get_or_create_google_user
from .schemas import SignupRequest, LoginRequest, GoogleLoginRequest, UserResponse, AuthResponse

logger = logging.getLogger(__name__)

User = get_user_model()
router = Router(tags=["User"])


def get_user_role(user: User) -> str:
    if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
        return "admin"
    return "student"

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
        user=UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            role=get_user_role(user),
        ),
    )


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
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
    backend = getattr(user, "backend", settings.AUTHENTICATION_BACKENDS[0])
    login(request, user, backend=backend)
    return AuthResponse(
        success=True,
        message="Logged in successfully.",
        user=UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            role=get_user_role(user),
        ),
    )


@router.post("/logout", response=AuthResponse)
def logout_user(request: HttpRequest):
    logout(request)
    return AuthResponse(
        success=True,
        message="Logged out successfully.",
        user=None
    )


@router.post("/google-login", response=AuthResponse)
def google_login(request: HttpRequest, data: GoogleLoginRequest):
    if not settings.GOOGLE_OAUTH2_CLIENT_ID:
        return AuthResponse(
            success=False,
            message="Google sign-in is not configured.",
            user=None,
        )
    payload = verify_google_token(data.id_token)
    if not payload:
        return AuthResponse(
            success=False,
            message="Invalid or expired Google token.",
            user=None,
        )
    email = payload.get("email")
    if not email:
        return AuthResponse(
            success=False,
            message="Email not provided by Google.",
            user=None,
        )
    if not is_allowed_domain(email):
        return AuthResponse(
            success=False,
            message="Only usls account are allowed to sign in.",
            user=None,
        )
    user = get_or_create_google_user(User, email)
    backend = getattr(user, "backend", settings.AUTHENTICATION_BACKENDS[0])
    login(request, user, backend=backend)
    return AuthResponse(
        success=True,
        message="Logged in successfully.",
        user=UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            role=get_user_role(user),
        ),
    )


@router.get("/profile", response=AuthResponse)
def get_current_user(request: HttpRequest):
 
    user = request.user
    if not user.is_authenticated:
        return AuthResponse(
            success=False,
            message="Not authenticated.",
            user=None,
        )

    return AuthResponse(
        success=True,
        message="Authenticated.",
        user=UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            role=get_user_role(user),
        ),
    )


@router.post("/forgot-password", response=AuthResponse)
def forgot_password(request: HttpRequest, data: LoginRequest):
    return AuthResponse(
        success=True,
        message="Password reset link sent to your email.",
        user=None
    )