# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_eventfeedpluginmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlearticleteaserpluginmodel',
            name='flavor',
            field=models.CharField(choices=[('action', 'Bold headings and action button'), ('link', 'Photo and read-more button'), ('simple', 'Simple')], max_length=8),
        ),
    ]