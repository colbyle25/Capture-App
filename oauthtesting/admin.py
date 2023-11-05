from django.contrib import admin
from oauthtesting.models import Account
from oauthtesting.models import POI
from oauthtesting.models import Message

# Register your models here.
admin.site.register(Account)
admin.site.register(POI)
admin.site.register(Message)