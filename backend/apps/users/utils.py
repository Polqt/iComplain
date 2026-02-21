from google.auth.exceptions import GoogleAuthError
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests as google_requests


def verify_google_token(id_token_str: str):
    try:
        return id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_OAUTH2_CLIENT_ID,
        )
    except (ValueError, GoogleAuthError) as e:
        return None
    
def is_allowed_domain(email: str) -> bool:
    domain = email.split('@')[-1] if "@" in email else ""
    return settings.ALLOWED_EMAIL_DOMAINS and domain in settings.ALLOWED_EMAIL_DOMAINS


def derive_name_from_email(email: str) -> str:

    local_part = (email or "").split("@")[0]
    if not local_part:
        return ""

    for sep in ["_", "-", "."]:
        local_part = local_part.replace(sep, " ")
    parts = [p for p in local_part.split(" ") if p]
    return " ".join(p.capitalize() for p in parts)


def get_or_create_google_user(User, email: str, name: str | None = None, avatar_url: str | None = None):
    user = User.objects.filter(email=email).first()
    if user is None:
        user = User(email=email)
        user.set_unusable_password()
    if name and not getattr(user, "full_name", ""):
        user.full_name = name
    if avatar_url and not getattr(user, "avatar_url", ""):
        user.avatar_url = avatar_url
    user.save()
    return user


# Avatar upload config
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}  # MIME types
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG', 'GIF', 'WEBP'}  # Pillow format names
ALLOWED_IMAGE_TYPES_DISPLAY = 'JPEG, PNG, GIF, or WebP'


def get_invalid_type_message() -> str:
    return f"Invalid file type. Please upload a {ALLOWED_IMAGE_TYPES_DISPLAY} image."


def get_file_too_large_message() -> str:
    size_mb = MAX_AVATAR_SIZE // (1024 * 1024)
    return f"File too large. Maximum size is {size_mb}MB."