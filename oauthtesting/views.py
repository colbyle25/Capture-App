from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .forms import AccountForm
from .models import Account

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

def profile_view(request):
  if request.method == 'POST':
    form = AccountForm(request.POST, request.FILES)
    if form.is_valid():
      username = form.cleaned_data['username']
      check_if_exists = Account.objects.filter(username=username)
      if check_if_exists.exists():
        check_if_exists.delete()
      form.save()
      account = form.instance
      return render(request, 'oauthtesting/profile.html', {'form': form, 'account': account})
  else:
    form = AccountForm()
    return render(request, 'oauthtesting/profile.html', {'form': form})
