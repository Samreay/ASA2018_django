# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0031_auto_20170125_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendee',
            options={'ordering': ['family_name', 'given_names']},
        ),
        migrations.AddField(
            model_name='regooption',
            name='asa_only',
            field=models.BooleanField(default=False, help_text=b'Tick this to restrict this option to ASA members only'),
        ),
    ]
