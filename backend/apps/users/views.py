import logging
import os
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.db import transaction
from ninja import Router, File
from ninja.files import UploadedFile
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest
from PIL import Image
from .utils import (
    verify_google_token,
    is_allowed_domain,
    get_or_create_google_user,
    derive_name_from_email,
    MAX_AVATAR_SIZE,
    ALLOWED_IMAGE_FORMATS,
    get_invalid_type_message,
    get_file_too_large_message,
)
from .schemas import LoginRequest, GoogleLoginRequest, ProfileUpdateRequest, UserResponse, AuthResponse

logger = logging.getLogger(__name__)

User = get_user_model()
router = Router(tags=["User"])

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

    # Ensure we have a display name stored (best-effort derived from email)
    if not getattr(user, "full_name", ""):
        user.full_name = derive_name_from_email(getattr(user, "email", "") or "")
        user.save(update_fields=["full_name"])

    backend = getattr(user, "backend", settings.AUTHENTICATION_BACKENDS[0])
    login(request, user, backend=backend)
    return AuthResponse(
        success=True,
        message="Logged in successfully.",
        user=UserResponse.model_validate(user, from_attributes=True),
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

    # Google token commonly provides "name" and "picture"
    name = payload.get("name") if isinstance(payload, dict) else None
    avatar_url = payload.get("picture") if isinstance(payload, dict) else None
    user = get_or_create_google_user(User, email, name=name, avatar_url=avatar_url)

    # Fallback if Google didn't provide a name
    if not getattr(user, "full_name", ""):
        user.full_name = derive_name_from_email(email)
        user.save(update_fields=["full_name"])

    backend = getattr(user, "backend", settings.AUTHENTICATION_BACKENDS[0])
    login(request, user, backend=backend)
    return AuthResponse(
        success=True,
        message="Logged in successfully.",
        user=UserResponse.model_validate(user, from_attributes=True),
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

    # Ensure we have a display name stored (best-effort derived from email)
    if not getattr(user, "full_name", ""):
        user.full_name = derive_name_from_email(getattr(user, "email", "") or "")
        user.save(update_fields=["full_name"])

    return AuthResponse(
        success=True,
        message="Authenticated.",
        user=UserResponse.model_validate(user, from_attributes=True),
    )


@router.patch("/profile", response=AuthResponse)
def update_profile(request: HttpRequest, data: ProfileUpdateRequest):
    user = request.user
    if not user.is_authenticated:
        return AuthResponse(
            success=False,
            message="Not authenticated.",
            user=None,
        )

    update_fields = []

    if data.name is not None:
        name = data.name.strip()
        if len(name) == 0:
            return AuthResponse(
                success=False,
                message="Name must not be empty.",
                user=None,
            )
        if len(name) > 150:
            return AuthResponse(
                success=False,
                message="Name must be 150 characters or fewer.",
                user=None,
            )
        user.full_name = name
        update_fields.append("full_name")

    if update_fields:
        user.save(update_fields=update_fields)

    return AuthResponse(
        success=True,
        message="Profile updated successfully.",
        user=UserResponse.model_validate(user, from_attributes=True),
    )


@router.post("/profile/avatar", response=AuthResponse)
def upload_avatar(request: HttpRequest, file: UploadedFile = File(...)):  # noqa: B008
    user = request.user
    if not user.is_authenticated:
        return AuthResponse(
            success=False,
            message="Not authenticated.",
            user=None,
        )

    if file.size > MAX_AVATAR_SIZE:
        return AuthResponse(
            success=False,
            message=get_file_too_large_message(),
            user=None,
        )

    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        if img.format not in ALLOWED_IMAGE_FORMATS:
            return AuthResponse(
                success=False,
                message=get_invalid_type_message(),
                user=None,
            )
    except Exception:
        return AuthResponse(
            success=False,
            message=get_invalid_type_message(),
            user=None,
        )

    old_avatar = user.avatar_file
    old_path = old_avatar.path if old_avatar else None

    user.avatar_file = file
    user.avatar_url = ""
    user.save(update_fields=["avatar_file", "avatar_url"])

    if old_path and old_path != user.avatar_file.path:
        transaction.on_commit(lambda: _safe_delete_file(old_path))

    return AuthResponse(
        success=True,
        message="Avatar uploaded successfully.",
        user=UserResponse.model_validate(user, from_attributes=True),
    )


def _safe_delete_file(path: str) -> None:
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError as e:
        logger.warning("Failed to delete old avatar file %s: %s", path, e)


@router.delete("/profile/avatar", response=AuthResponse)
def delete_avatar(request: HttpRequest):
    user = request.user
    if not user.is_authenticated:
        return AuthResponse(
            success=False,
            message="Not authenticated.",
            user=None,
        )

    old_path = user.avatar_file.path if user.avatar_file else None

    user.avatar_file = None
    user.avatar_url = ""
    user.save(update_fields=["avatar_file", "avatar_url"])

    if old_path:
        transaction.on_commit(lambda: _safe_delete_file(old_path))

    return AuthResponse(
        success=True,
        message="Avatar removed.",
        user=UserResponse.model_validate(user, from_attributes=True),
    )
