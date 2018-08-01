# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0020_auto_20161207_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='', help_text=b'Address or other simple location of the event (you can add more description, Google Maps etc. in the event description', max_length=300, blank=True),
            preserve_default=False,
        ),
    ]
