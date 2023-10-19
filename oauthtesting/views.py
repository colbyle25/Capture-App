from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.messages import *
from .forms import AccountForm
from .models import Account
from django.conf import settings


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account.exists():
            account = account.first()
        else:
            account = Account(username=request.user, bio="", points=0, picture="")
            account.save()
        context = {'user': request.user, 'account': account}
        return render(request, 'oauthtesting/index.html', context)
    return HttpResponseRedirect("/login/")


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render(request, "oauthtesting/login.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def profile_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            points = 0  # Default value in case the account doesn't already exist in the database for some reason
            check_if_exists = Account.objects.filter(username=request.user)
            if check_if_exists.exists():
                points = check_if_exists.first().points
                check_if_exists.delete()
            updated = form.save(commit=False)
            updated.username = request.user
            updated.points = points
            updated.save()
            # Send a message to the user to let them know they did something
            messages.success(request, 'Successfully updated profile')
            return HttpResponseRedirect("/")
    else:
        form = AccountForm()
        return render(request, 'oauthtesting/profile.html', {'form': form})


def map(request):
    api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'oauthtesting/map.html', {'api_key': api_key})
