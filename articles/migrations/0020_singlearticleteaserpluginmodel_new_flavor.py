# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-08 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20171207_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlearticleteaserpluginmodel',
            name='new_flavor',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Bold headings and action button'), (2, 'Photo and read-more button'), (3, 'Simple')], default=1),
        ),
    ]
