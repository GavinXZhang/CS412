# Generated by Django 5.1.2 on 2024-11-10 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='DOR',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='PNumber',
            field=models.TextField(),
        ),
    ]