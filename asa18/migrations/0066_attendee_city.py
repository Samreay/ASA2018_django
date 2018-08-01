# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0065_auto_20170316_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='city',
            field=models.CharField(default=b'', help_text=b'Suburb/town/city', max_length=100, blank=True),
        ),
    ]
