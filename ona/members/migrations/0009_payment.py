# Generated by Django 5.0 on 2024-01-23 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_refno', models.CharField(max_length=100)),
                ('pay_amount', models.CharField(max_length=10)),
                ('pay_date', models.DateField(null=True)),
                ('pay_status', models.CharField(default='pending', max_length=30)),
                ('pay_memberId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('pay_subId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.sub')),
            ],
        ),
    ]
