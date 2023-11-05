from django.contrib import admin
from oauthtesting.models import Account, TextMessage
from oauthtesting.models import POI
from oauthtesting.models import Message

# Register your models here.
admin.site.register(Account)
admin.site.register(POI)


@admin.action(description='Approve selected messages')
def approve_messages(queryset):
    queryset.update(approved=True)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'time', 'longitude', 'latitude', 'approved')
    list_filter = ('approved',)
    actions = [approve_messages]


admin.site.register(TextMessage, MessageAdmin)