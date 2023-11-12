"""
URL configuration for capture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from oauthtesting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('pointshop/', views.pointshop, name='pointshop'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lookup/', views.lookup, name='lookup'),
    path('map/', views.map, name='map'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/settings/apply/', views.apply_profile_settings, name='apply_profile_settings'),
    path('', views.home, name='home'),
    path('save_marker/', views.save_marker, name='save_marker'),
    path('delete_marker/<int:marker_id>/', views.delete_marker, name='delete_marker'),
    path('load_markers/', views.load_markers, name='load_markers'),
    path('like/<int:id>/', views.like_marker, name='like'),
    path('unlike/<int:id>/', views.unlike_marker, name='unlike'),
    path('approve/<int:id>/', views.approve_marker, name='approve'),
    path('unapprove/<int:id>/', views.unapprove_marker, name='unapprove'),
    path('amiadmin/', views.amiadmin, name='amiadmin'),
]

# Allows for seeing profile pictures in development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
