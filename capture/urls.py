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
from oauthtesting import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lookup/', views.lookup, name='lookup'),
    path('map/', views.map, name='map'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.home, name='home')
]

# Allows for seeing profile pictures in development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
