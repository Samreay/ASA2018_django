# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0011_auto_20161201_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='publish_attendees',
            field=models.BooleanField(default=False, help_text=b'Check this to activate the automated attendee reporting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='publish_diversity',
            field=models.BooleanField(default=False, help_text=b'Check this to activate the automated diversity reporting'),
            preserve_default=True,
        ),
    ]
