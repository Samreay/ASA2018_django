# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0036_auto_20170130_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='status',
            field=models.CharField(default=b's', max_length=1, choices=[(b's', b'Submitted'), (b'a', b'Accepted'), (b'd', b'Demoted'), (b'r', b'Rejected')]),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='time_end',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='time_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='type',
            field=models.CharField(default=b't', max_length=1, choices=[(b't', b'Talk'), (b'p', b'Poster')]),
        ),
    ]
