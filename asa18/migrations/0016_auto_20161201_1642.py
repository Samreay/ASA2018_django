# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0015_auto_20161201_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['time_start', 'time_end']},
        ),
        migrations.AlterModelOptions(
            name='prize',
            options={'ordering': ['name', 'meeting']},
        ),
        migrations.AddField(
            model_name='meeting',
            name='program_release_date',
            field=models.DateTimeField(help_text=b'Date and time at which to release the meeting program. Leave blank to not release the program', null=True, blank=True),
            preserve_default=True,
        ),
    ]
