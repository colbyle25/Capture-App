# https://stackoverflow.com/questions/60271748/how-to-pass-a-variable-from-views-to-base-html-in-django
from .models import Account, Account_Profile

def add_background_to_context(request):
    if not request.user.is_authenticated:
        return {}
    try:
        user = Account.objects.filter(username=request.user).first()
        user_profile = Account_Profile.objects.filter(user=user).first()
        background_color = user_profile.background.css if user_profile.background else None
        return {'background_color': background_color}
    except:
        return {}

