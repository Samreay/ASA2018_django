# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0032_auto_20170125_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='is_nz_astro',
            field=models.BooleanField(default=False, help_text=b'Tick if you are *not* an ASA member, but you are based in New Zealand'),
        ),
        migrations.AddField(
            model_name='regooption',
            name='nz_only',
            field=models.BooleanField(default=False, help_text=b'Tick this to restrict this option to NZ astronomer'),
        ),
    ]
