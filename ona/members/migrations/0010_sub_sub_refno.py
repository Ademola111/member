# Generated by Django 5.0 on 2024-01-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub',
            name='sub_refno',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
