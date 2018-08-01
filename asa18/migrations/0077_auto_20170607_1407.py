# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0076_session_extended_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'ordering': ('time_start', 'time_end', 'presenter', 'title')},
        ),
    ]
