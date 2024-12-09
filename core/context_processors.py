def is_development(request):
    allowed_hosts = ["localhost", "rm", "127.0.0.1"]
    return {
        'is_development': request.get_host() in allowed_hosts
    }
