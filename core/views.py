from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def cv(request):
    return render(request, 'cv.html')
