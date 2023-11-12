from django.contrib import admin
from oauthtesting.models import Account, TextMessage, POI, Item, Purchase

# Register your models here.
admin.site.register(Account)
admin.site.register(POI)
admin.site.register(Item)
admin.site.register(Purchase)

@admin.action(description='Approve selected messages')
def approve_messages(modeladmin, request, queryset):
    queryset.update(approved=True)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'time', 'longitude', 'latitude', 'approved')
    list_filter = ('approved',)
    actions = [approve_messages]


admin.site.register(TextMessage, MessageAdmin)