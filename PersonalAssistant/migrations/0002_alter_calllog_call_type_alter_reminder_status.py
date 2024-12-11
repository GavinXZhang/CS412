# Generated by Django 5.1.3 on 2024-12-09 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalAssistant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calllog',
            name='call_type',
            field=models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('missed', 'Missed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='status',
            field=models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], default=False),
        ),
    ]