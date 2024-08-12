from django.contrib import admin

# Register your models here.
from sign.models import Event, Guest


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name']
    search_fields = ['address']
    list_filter = ['status']


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']



admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)