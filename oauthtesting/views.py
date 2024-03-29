from datetime import datetime
import json
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q

from django.apps import apps

from collections import defaultdict

from .forms import AccountForm
from .models import Account, TextMessage, POI, Item, Purchase, Account_Profile, Like
from .poihandling import *
from .tickethandling import *


# Create your views here.
@transaction.atomic
def home(request):
    upd_all()
    if request.method == 'SEARCH':
        print("Search!")
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account.exists():
            account = account.first()
        else:
            account = Account(username=request.user, bio="", points=0, picture="")
            account.save()
        account_profile, created = Account_Profile.objects.get_or_create(user=account)
        border_color = account_profile.border.css if account_profile.border else None
        context = {'user': request.user, 'account': account, 'border': border_color}
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
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


def profile_settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")

    user = Account.objects.filter(username=request.user).first()
    purchases = Purchase.objects.filter(user=user).select_related('item')
    categorized_items = defaultdict(list)

    for purchase in purchases:
        categorized_items[purchase.item.category].append(purchase.item)

    user_profile, created = Account_Profile.objects.get_or_create(user=user)
    selected_items = defaultdict(list)
    if not created:
        for category_name, _ in Item.CATEGORY_CHOICES:
            selected_items[category_name].append(getattr(user_profile, category_name, None))

    return render(request, 'oauthtesting/profile_settings.html',
                  {'user': user, 'categorized_items': dict(categorized_items), 'selected_items': dict(selected_items)})


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def apply_profile_settings(request):
    data = json.loads(request.body)
    user = Account.objects.filter(username=request.user).first()
    user_profile = Account_Profile.objects.filter(user=user).first()

    if not user_profile:
        return JsonResponse({'success': False, 'error': 'User profile does not exist.'}, status=404)

    for category, item_id in data.items():
        if item_id == 'None':
            setattr(user_profile, category, None)
        else:
            item = get_object_or_404(Item, id=item_id)
            setattr(user_profile, category, item)

    user_profile.save()
    messages.success(request, 'Successfully updated profile')
    return JsonResponse({'success': True})


@transaction.atomic
def map(request):
    upd_all()
    api_key = settings.GOOGLE_MAPS_API_KEY
    pois = POI.objects.all()

    time_format = ' %I:%H:%M %p %m-%d-%Y'

    pois_list = []
    for poi in pois:
        poi_data = {
            'pid': poi.pid,
            'points': poi.points,
            'img': poi.img.url,
            'time': poi.time.strftime(time_format),
            'latitude': float(poi.latitude),
            'longitude': float(poi.longitude),
            'name': poi.name,
            'owner': poi.owner
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
    context = {'account': None, 'latest_message': None, 'latest_message_content': None}
    if request.method == 'GET':
        username_query = request.GET.get('lookup')
        print("user: " + username_query)
        try:
            account = Account.objects.get(username=username_query)
            context['account'] = account
            latest_message = TextMessage.objects.filter(username=account, approved=True).order_by('-time').first()
            if latest_message:
                context['latest_message'] = latest_message
                context['latest_message_content'] = parse_message_content(latest_message.message)
        except Account.DoesNotExist:
            print("Account not found")

    return render(request, 'oauthtesting/lookup.html', context)


@transaction.atomic
def leaderboard(request):
    upd_all()
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


@transaction.atomic
def pointshop(request):
    upd_all()
    items = Item.objects.all()
    user = Account.objects.filter(username=request.user).first()
    purchased_item_ids = Purchase.objects.filter(user=user).values_list('item_id', flat=True)

    categorized_items = defaultdict(list)
    for item in items:
        categorized_items[item.category].append(item)
    
    
    quants = defaultdict(int)
    for purc in Purchase.objects.filter(user=user):
        quants[purc.item.name] += 1
    qs = [(a, quants[a]) for a in quants]

    return render(request, 'oauthtesting/pointshop.html', {
        'account': Account.objects.filter(username=request.user).first(),
        'categorized_items': dict(categorized_items),
        'quants': qs,
        'purchased_item_ids': purchased_item_ids})


@require_http_methods(["POST"])
@transaction.atomic
def purchase_item(request, item_id):
    upd_all()
    item = Item.objects.get(id=item_id)
    user = Account.objects.filter(username=request.user).first()
    if user.points >= item.cost:
        user.points -= item.cost
        user.save()

        Purchase.objects.create(user=user, item=item)
        return JsonResponse({'success': True,
                             'new_points_total': user.points})
    else:
        return JsonResponse({'success': False, 'error': 'Not enough points'})


@require_http_methods(["POST"])
@transaction.atomic
def save_marker(request):
    data = json.loads(request.body)
    username = Account.objects.filter(username=request.user).first()
    if not eat_ticket(username):
        return JsonResponse({'status': 'not enough tickets!'})
    message = data['message']
    latitude = data['latitude']
    longitude = data['longitude']

    marker_message = TextMessage.objects.create(
        username=username,
        message=message,
        latitude=latitude,
        longitude=longitude,
        time=datetime.now()
    )
    return JsonResponse({'id': marker_message.id, 'status': 'success'})


@login_required
@require_http_methods(["DELETE"])
def delete_marker(request, marker_id):
    marker = get_object_or_404(TextMessage, pk=marker_id)
    me = Account.objects.filter(username=request.user).first()
    if (marker.username != me
            and not request.user.is_superuser):
        return HttpResponse(status=403)
    marker.delete()
    return JsonResponse({'status': 'success', 'message': 'Marker deleted'})


@login_required
def approve_marker(request, id):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    marker = get_object_or_404(TextMessage, pk=id)
    if marker.rejected:
        return JsonResponse({'status': 'failure', 'message': 'Marker already rejected!'})
    marker.approved = True
    marker.save()
    return JsonResponse({'status': 'success', 'message': 'Marker approved'})


@login_required
def unapprove_marker(request, id):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    marker = get_object_or_404(TextMessage, pk=id)
    marker.approved = False
    marker.save()
    return JsonResponse({'status': 'success', 'message': 'Marker unapproved'})


@login_required
def load_markers(request):
    markers = TextMessage.objects.filter(
        Q(approved=True) | Q(username=request.user.username)) if not request.user.is_superuser else TextMessage.objects.filter()
    markers_data = list(markers.values('id', 'latitude', 'longitude', 'message', 'approved', 'rejected', 'rejection_reason'))
    for x in markers_data:
        mk = TextMessage.objects.get(id=x['id'])
        i = x['id']
        x['likes'] = Like.objects.filter(poster=mk).count()
        x['liked'] = Like.objects.filter(poster=mk,
                                         liker=Account.objects.filter(username=request.user).first()).count() > 0
    return JsonResponse(markers_data, safe=False)


@login_required
def like_marker(request, id):
    marker = get_object_or_404(TextMessage, pk=id)
    username = Account.objects.filter(username=request.user).first()
    if Like.objects.filter(liker=username, poster=marker).count():
        return HttpResponseBadRequest()
    Like.objects.create(
        poster=marker,
        liker=username
    )
    return JsonResponse({'status': 'success', 'message': 'Like added'})


@login_required
def unlike_marker(request, id):
    marker = get_object_or_404(TextMessage, pk=id)
    username = Account.objects.filter(username=request.user).first()
    if not Like.objects.filter(liker=username, poster=marker).count():
        return HttpResponseBadRequest()
    like = get_object_or_404(Like, liker=username, poster=marker)
    like.delete()
    return JsonResponse({'status': 'success', 'message': 'Like removed'})


@login_required
def amiadmin(request):
    return JsonResponse({'admin': request.user.is_superuser})


def admin_approval(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")

    sort_by = request.GET.get('sort', '-time')  # Default sort is by time in descending order
    if sort_by not in ['username', 'time', 'message', 'approved', 'rejected', '-time', '-username', '-message', '-approved', '-rejected']:
        sort_by = '-time'

    text_message_list = TextMessage.objects.all().order_by(sort_by)

    if request.method == 'POST':
        message_ids = request.POST.getlist('message_ids')
        for id in message_ids:
            message = TextMessage.objects.get(id=id)
            message.approved = request.POST.get(f'approved_{id}', 'false') == 'true'
            if request.POST.get(f'rejected_{id}', 'false') == 'true':
                message.approved = False
                message.rejected = True
                message.rejection_reason = request.POST.get(f'rejection_reason_{id}', '')
            else:
                message.rejected = False
            message.save()

        messages.success(request, 'Successfully updated messages')

    for message in text_message_list:
        message.processed_content = parse_message_content(message.message)
    return render(request, 'oauthtesting/admin_approval.html', {'text_message_list': text_message_list})


def parse_message_content(message):
    words = message.split()
    parsed_content = []

    for word in words:
        if word.startswith("http"):
            if "youtube.com" in word:
                embed_url = word.replace("watch?v=", "embed/").replace("shorts/", "embed/")
                parsed_content.append({'type': 'youtube', 'url': embed_url})
            else:
                parsed_content.append({'type': 'url', 'url': word})
        else:
            parsed_content.append({'type': 'text', 'text': word})

    return parsed_content

@login_required
@transaction.atomic
def claim_poi(request, pid):
    upd_all()
    poi = get_object_or_404(POI, pid=pid)
    poi.owner=Account.objects.filter(username=request.user).first().username
    poi.save()
    return HttpResponseRedirect("/map")

@login_required
def reject_marker(request, pid):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    data = json.loads(request.body)
    marker = get_object_or_404(Message, pid=pid)
    marker.approved = False
    marker.rejected = True
    marker.rejection_reason = data['reason']
    marker.save()
    return JsonResponse({'success' : True, 'message': 'Successfully rejected'})

@login_required
def unreject_marker(request, pid):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    marker = get_object_or_404(Message, pid=pid)
    marker.rejected = False
    marker.rejection_reason = ""
    marker.save()
    return JsonResponse({'success' : True, 'message': 'Successfully un-rejected'})
