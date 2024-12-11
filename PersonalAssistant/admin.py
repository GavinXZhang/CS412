
from .models import CalendarEvent
# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(CallLog)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'user']

    def save_model(self, request, obj, form, change):
        print(f"Saving CalendarEvent: {form.cleaned_data}")
        super().save_model(request, obj, form, change)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['message', 'reminder_time', 'status', 'user']
