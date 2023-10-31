from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.messages import *
from .forms import AccountForm
from .models import Account
from .models import POI
from django.conf import settings
import json


# Create your views here.

def home(request):
    if request.method == 'SEARCH':
        print("Search!")
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
    pois = POI.objects.all()

    time_format = ' %I:%H:%M %p %m-%d-%Y'

    pois_list = []
    for poi in pois:
        poi_data = {
            'pid':  poi.pid,
            'points': poi.points,
            'img': poi.img.url,
            'time': poi.time.strftime(time_format),
            'latitude': float(poi.latitude),
            'longitude': float(poi.longitude),
            'name': poi.name,
        }
        pois_list.append(poi_data)

    pois_json = json.dumps(pois_list)

    account = Account.objects.filter(username=request.user)
    if account.exists():
        account = account.first()
    else:
        account = None

    return render(request, 'oauthtesting/map.html', {'api_key': api_key, 'pois': pois_json, 'account': account})


def lookup(request):
    if request.method == 'GET':
        info = request.GET.get('lookup')
        print("user: " + info)
        account = Account.objects.filter(username=info)
        if account.exists():
            account = account.first()
        else:
            account = None
        return render(request, 'oauthtesting/lookup.html', {'account': account})


def leaderboard(request):
    accounts = Account.objects.all().order_by('-points')
    placement = -1
    account = None
    for i in range(len(accounts)):
        if str(accounts[i].username) == str(request.user):
            placement = i + 1
            account = accounts[i]
            if i < 5:  # Don't render the user in two places
                account = None
            break
    context = {'accounts': accounts[:5], 'account': account, 'placement': placement}
    return render(request, 'oauthtesting/leaderboard.html', context)

