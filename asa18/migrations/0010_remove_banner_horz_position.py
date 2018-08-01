# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0009_auto_20161130_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='horz_position',
        ),
    ]
