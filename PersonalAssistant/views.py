from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .models import CalendarEvent, Reminder,CallLog
from django.shortcuts import render
from datetime import date
from .utils import *
from datetime import datetime
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import AnonymousUser
import calendar
from datetime import date

class CalendarEventDeleteView(DeleteView):
    model = CalendarEvent
    template_name = 'PersonalAssistant/event_delete.html'
    success_url = reverse_lazy('event-list')  # Redirect to the event list after deletion
    
def HomePageView(request):
    today = datetime.now()
    year = today.year
    month = today.month

    if request.user.is_authenticated:
        # Fetch data for the logged-in user
        events = CalendarEvent.objects.filter(user=request.user, end_time__gte=today)
        reminders = Reminder.objects.filter(user=request.user, reminder_time__gte=today, status=False)
        missed_calls = CallLog.objects.filter(user=request.user, call_type="missed")
    else:
        # No user-specific data for anonymous users
        events = []
        reminders = []
        missed_calls = []

    # Generate the calendar grid with events
    calendar_data = get_month_calendar(year, month, events)

    # Generate summary synchronously
    summary = generate_summary(request.user, events, reminders, missed_calls)

    context = {
        'events': events,
        'reminders': reminders,
        'missed_calls': missed_calls,
        'calendar_data': calendar_data,
        'month': month,
        'year': year,
        'summary': summary
    }
    return render(request, 'PersonalAssistant/home.html', context)


class CallLogForm(forms.ModelForm):
    class Meta:
        model = CallLog
        fields = ['contact_name', 'phone_number', 'call_time', 'duration', 'call_type']
        widgets = {
            'call_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['message', 'reminder_time', 'status', 'calendar_event']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReminderCreateView(LoginRequiredMixin,CreateView):
    model = Reminder
    form_class = ReminderForm  # Use the custom form for datetime-local input
    template_name = 'PersonalAssistant/add_reminder.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        return super().form_valid(form)

class ReminderDeleteView(DeleteView):
    model = Reminder
    template_name = 'PersonalAssistant/reminder_confirm_delete.html'
    success_url = reverse_lazy('event-list')
class CallLogCreateView(LoginRequiredMixin,CreateView):
    model = CallLog
    form_class = CallLogForm  # Use the custom form for datetime-local input
    template_name = 'PersonalAssistant/add_call_log.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        return super().form_valid(form)

class CallLogDeleteView(DeleteView):
    model = CallLog
    template_name = 'PersonalAssistant/call_log_confirm_delete.html'
    success_url = reverse_lazy('event-list')
class CalendarEventListView(ListView):
    model = CalendarEvent
    template_name = 'PersonalAssistant/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Fetch user-specific events
            return CalendarEvent.objects.filter(user=self.request.user)
        else:
            # Return an empty queryset for anonymous users
            return CalendarEvent.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Fetch related reminders and call logs for authenticated users
            context['reminders'] = Reminder.objects.filter(user=self.request.user)
            context['call_logs'] = CallLog.objects.filter(user=self.request.user)
        else:
            # Provide empty context for anonymous users
            context['reminders'] = []
            context['call_logs'] = []
        return context
class CalendarEventDetailView(DetailView):
    model = CalendarEvent
    template_name = 'PersonalAssistant/event_detail.html'


class ReminderListView(ListView):
    model = Reminder
    template_name = 'PersonalAssistant/reminder_list.html'
    context_object_name = 'reminders'


class ReminderDetailView(DetailView):
    model = Reminder
    template_name = 'PersonalAssistant/reminder_detail.html'


class CalendarEventCreateView(LoginRequiredMixin, CreateView):
    model = CalendarEvent
    template_name = 'PersonalAssistant/add_event.html'
    form_class = CalendarEventForm  # Use the custom form for date/time input
    success_url = reverse_lazy('event-list')  # Redirect after successful creation

    def form_valid(self, form):
        # Automatically assign the logged-in user
        print("Form data collected by the server:")
        for key, value in form.cleaned_data.items():
            print(f"{key}: {value}")
        form.instance.user = self.request.user
        return super().form_valid(form)
