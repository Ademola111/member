# Generated by Django 5.0 on 2024-01-21 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_member_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='pic',
        ),
    ]
