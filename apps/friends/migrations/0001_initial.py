# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0003_remove_user_friend'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.ManyToManyField(related_name='friends', to='login.User')),
            ],
        ),
    ]
