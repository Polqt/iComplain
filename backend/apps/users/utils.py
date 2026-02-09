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

def get_or_create_google_user(User, email):
    user = User.objects.filter(email=email).first()
    if user is None:
        user = User(email=email)
        user.set_unusable_password()
        user.save()
    return user