import logging
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_APP_ORIGINS = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "https://tauri.localhost,"
    "tauri://localhost"
)


def _split_env_list(name: str, default: str = "") -> list[str]:
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _normalize_host(value: str) -> str:
    trimmed = value.strip()
    if not trimmed:
        return ""

    if "://" not in trimmed:
        trimmed = f"https://{trimmed}"

    parsed = urlparse(trimmed)
    return parsed.hostname or trimmed.split("/")[0].split(":")[0]


def _normalize_origin(value: str) -> str:
    trimmed = value.strip().rstrip("/")
    if not trimmed:
        return ""

    if "://" not in trimmed:
        scheme = "http" if trimmed.startswith(
            ("localhost", "127.0.0.1")) else "https"
        trimmed = f"{scheme}://{trimmed}"

    parsed = urlparse(trimmed)
    if not parsed.scheme or not parsed.netloc:
        return ""

    return f"{parsed.scheme}://{parsed.netloc}"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is required. Set it in .env or your environment.")
DEBUG = os.getenv('DEBUG', 'False') == 'True'

_allowed_hosts = _split_env_list('ALLOWED_HOSTS')
_allowed_hosts.extend(
    filter(
        None,
        [
            os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip(),
            "localhost",
            "127.0.0.1",
            ".onrender.com",
        ],
    )
)
ALLOWED_HOSTS = _dedupe(
    [host for host in (_normalize_host(value)
                       for value in _allowed_hosts) if host]
)
NINJA_SKIP_SESSION_AUTH_CSRF = False

# Google OAuth (school email sign-in)
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID', '')
_allowed_domains_raw = os.getenv('ALLOWED_EMAIL_DOMAINS', 'usls.edu.ph')
ALLOWED_EMAIL_DOMAINS = [d.strip()
                         for d in _allowed_domains_raw.split(',') if d.strip()]

# Validate at startup: warn if domains are empty while Google OAuth is configured
_logger = logging.getLogger(__name__)
if not ALLOWED_EMAIL_DOMAINS and GOOGLE_OAUTH2_CLIENT_ID:
    _logger.warning(
        "ALLOWED_EMAIL_DOMAINS is empty but GOOGLE_OAUTH2_CLIENT_ID is set; "
        "all Google logins will be rejected. Set ALLOWED_EMAIL_DOMAINS in .env."
    )

# Application definition

_cloudinary_url = os.getenv("CLOUDINARY_URL", "").strip()
_use_cloudinary = bool(_cloudinary_url)

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *(['cloudinary_storage', 'cloudinary'] if _use_cloudinary else []),
    'corsheaders',
    'ninja',
    'channels',
    'apps.users',
    'apps.tickets',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'config.middleware.request_logging',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'config.middleware.disable_csrf',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ninja.compatibility.files.fix_request_files_middleware'
]

# Cross-origin: frontend uses credentials: 'include'.
# Never use CORS_ALLOW_ALL_ORIGINS with CORS_ALLOW_CREDENTIALS in production.
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
_cors_origins = _split_env_list('CORS_ALLOWED_ORIGINS', DEFAULT_APP_ORIGINS)
_cors_origins.extend(_split_env_list('APP_ORIGINS'))
if os.getenv("FRONTEND_URL", "").strip():
    _cors_origins.append(os.getenv("FRONTEND_URL", "").strip())

CORS_ALLOWED_ORIGINS = _dedupe(
    [origin for origin in (_normalize_origin(value)
                           for value in _cors_origins) if origin]
)
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-language",
    "content-type",
    "origin",
    "x-csrftoken",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

# Session cookie: SameSite=None requires Secure=True (browsers drop the cookie otherwise).
# In local HTTP dev, use Lax; in production over HTTPS, use None + Secure.
if DEBUG:
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

AUTH_USER_MODEL = 'users.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

_redis_url = os.getenv("REDIS_URL", "").strip()
_use_redis_channels = bool(_redis_url) and _redis_url.startswith(
    ("redis://", "rediss://", "unix://"))

if DEBUG or not _use_redis_channels:
    if not DEBUG and not _use_redis_channels:
        _logger.warning(
            "REDIS_URL is missing or invalid for Channels; falling back to InMemoryChannelLayer. "
            "Realtime events will only work reliably within a single process."
        )
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [_redis_url],
            },
        }
    }

ASGI_APPLICATION = 'config.asgi.application'
WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# Supports DATABASE_URL (used by Railway) or individual DB_* env vars.

_database_url = os.getenv('DATABASE_URL', '').strip()
if _database_url:
    _parsed = urlparse(_database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _parsed.path.lstrip('/'),
            'USER': _parsed.username or '',
            'PASSWORD': _parsed.password or '',
            'HOST': _parsed.hostname or 'localhost',
            'PORT': str(_parsed.port or 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Cache: LocMem for single-process dev; set CACHE_URL (e.g. redis://) in production for multi-process.
_cache_url = os.getenv("CACHE_URL", "").strip()
if _cache_url and _cache_url.startswith("redis://"):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _cache_url,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media / file uploads
# When CLOUDINARY_URL is set, use Cloudinary for persistent cloud storage.
# Otherwise fall back to local filesystem (dev only — ephemeral on Render).
if _use_cloudinary:
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': _cloudinary_url}
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure MEDIA_ROOT is always defined (used by urls.py static() in dev)
if 'MEDIA_ROOT' not in dir():
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CSRF exemptions -- only exempt truly public/token-auth endpoints
CSRF_EXEMPT_API_PREFIXES = [
    '/api/user/register',  # Public signup
    '/api/user/login',     # Public login
    '/api/user/google-login',  # Google OAuth (token-based, not session)
    '/api/webhooks/',       # Third-party webhooks using token signatures
]


# Celery configuration
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "")

if not DEBUG and EMAIL_BACKEND.endswith("smtp.EmailBackend"):
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        _logger.warning(
            "EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are not set; "
            "email sending will fail in production."
        )
