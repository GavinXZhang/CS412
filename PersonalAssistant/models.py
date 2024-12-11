

from django.urls import reverse

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def clean(self):
        # Ensure start_time is earlier than end_time
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be earlier than end time.")


class Reminder(models.Model):
    """
    Model to represent reminders for a user.
    Can optionally link to a CalendarEvent.
    """
    STATUS_CHOICES = [
        (False, 'Pending'),
        (True, 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders')
    message = models.TextField()
    reminder_time = models.DateTimeField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)  # False = pending, True = completed

    def __str__(self):
        return f"Reminder for {self.user.username}: {self.message}"

    def clean(self):
        # Ensure reminder_time is in the future
        from django.utils.timezone import now
        if self.reminder_time and self.reminder_time < now():
            raise ValidationError("Reminder time must be in the future.")

class CallLog(models.Model):
    """
    Model to log call details for a user.
    """
    CALL_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
        ('missed', 'Missed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='call_logs')
    contact_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    call_time = models.DateTimeField()
    duration = models.PositiveIntegerField()  # Duration in seconds
    call_type = models.CharField(max_length=50, choices = CALL_CHOICES)  # E.g., incoming, outgoing, missed

    def __str__(self):
        return f"CallLog for {self.user.username}: {self.contact_name} ({self.call_type})"
