from django.shortcuts import render

from main.const_data.actual_urls import ACTUAL_URLS


def index(request):
    return render(request, 'main/index.html')


def apis_info(request):
    return render(request, 'main/apis-info.html', {'actual_urls': ACTUAL_URLS})
