# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0038_auto_20170130_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 30, 17, 29, 38, 771488), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presentation',
            name='submitted',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 30, 17, 29, 45, 104516), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 30, 17, 29, 47, 620102), auto_now_add=True),
            preserve_default=False,
        ),
    ]
