from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("hello world youre at the polls index")