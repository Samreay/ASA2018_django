# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0034_auto_20170127_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='meeting',
            field=models.ForeignKey(to='asa18.Meeting'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='meeting_rego',
            field=models.ForeignKey(default=None, blank=True, to='asa18.RegoOption', null=True),
        ),
    ]
