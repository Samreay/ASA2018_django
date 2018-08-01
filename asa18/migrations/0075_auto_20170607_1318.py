# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0074_session_blurb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='blurb',
            field=models.CharField(help_text=b'Short blurb about session contents', max_length=50, blank=True),
        ),
    ]
