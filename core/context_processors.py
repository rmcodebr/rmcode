def is_development(request):
    # print(request.get_host())
    allowed_hosts = ["localhost:8000", "127.0.0.1:8000"]
    return {
        'is_development': request.get_host() in allowed_hosts
    }
