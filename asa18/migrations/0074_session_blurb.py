# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0073_auto_20170606_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='blurb',
            field=models.CharField(help_text=b'Short blurb about session contents', max_length=300, blank=True),
        ),
    ]
