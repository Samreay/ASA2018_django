# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0037_auto_20170130_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='session',
            field=models.ForeignKey(blank=True, to='asa18.Session', null=True),
        ),
    ]
