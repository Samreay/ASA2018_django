# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0017_event_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 7, 4, 15, 52, 438283, tzinfo=utc), help_text=b'Time this event should be made publically available'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='rego_closes',
            field=models.DateTimeField(help_text=b'Leave blankt to use the rego opening date of the related event(s)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='rego_opens',
            field=models.DateTimeField(help_text=b'Leave blank to use the rego opening date of the related event(s)', null=True, blank=True),
            preserve_default=True,
        ),
    ]
