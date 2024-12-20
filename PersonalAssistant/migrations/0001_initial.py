# Generated by Django 5.1.3 on 2024-11-25 05:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('call_time', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
                ('call_type', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('reminder_time', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('calendar_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reminders', to='PersonalAssistant.calendarevent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
