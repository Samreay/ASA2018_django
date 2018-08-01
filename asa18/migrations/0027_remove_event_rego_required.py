# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0026_auto_20170116_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='rego_required',
        ),
    ]
