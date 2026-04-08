import json
import logging
import time
import uuid
from typing import Callable

from django.conf import settings


UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
CSRF_EXEMPT_API_PREFIXES = tuple(
    getattr(settings, "CSRF_EXEMPT_API_PREFIXES", ()))
logger = logging.getLogger("request")


# checks the path and returns True if the path starts with any prefix mentioned in CSRF_EXEMPT_API.
def _is_exempt_api_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in CSRF_EXEMPT_API_PREFIXES)

# detector for non-cookie authentication; checks HTTP_AUTHORIZATION and HTTP_X_API_KEY


def _has_non_cookie_auth(request) -> bool:
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    api_key_header = request.META.get("HTTP_X_API_KEY", "")

    if auth_header and auth_header.startswith(("Bearer ", "Token ")):
        return True

    if api_key_header and len(api_key_header) >= 16:
        return True

    return False


def disable_csrf(get_response: Callable):
    """Middleware that selectively disables CSRF checks for API endpoints that:
    - check conditions if request.method is in UNSAFE_METHODS
    - check if request.path matches an exempt prefix
    - if all True set request._dont_enforce_csrf_checks = True to disable CSRF checks for that request
    """

    def middleware(request):
        if (
            request.method in UNSAFE_METHODS
            and _is_exempt_api_path(request.path)
            and _has_non_cookie_auth(request)
        ):
            setattr(request, "_dont_enforce_csrf_checks", True)

        return get_response(request)

    return middleware


def request_logging(get_response: Callable):
    def middleware(request):
        started = time.perf_counter()
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id

        response = get_response(request)

        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response["X-Request-ID"] = request_id

        logger.info(
            json.dumps(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                }
            )
        )

        return response

    return middleware
