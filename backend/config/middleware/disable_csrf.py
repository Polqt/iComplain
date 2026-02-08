def disable_csrf(get_response):
    def middleware(request):
        if request.path.startswith("/api/"):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return get_response(request)
    return middleware
