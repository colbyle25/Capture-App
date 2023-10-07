from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        context = {'user': request.user}
        return render(request, 'oauthtesting/index.html', context)
    return HttpResponseRedirect("/login/")
  
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render(request, "oauthtesting/login.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")