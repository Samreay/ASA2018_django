# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0018_auto_20161207_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='rego_opens',
        ),
    ]
