# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0041_auto_20170131_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventattendance',
            name='attendee',
        ),
        migrations.RemoveField(
            model_name='eventattendance',
            name='event',
        ),
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(default=b'D2ObwlUipeYBf3IRShM29srsZiekJx', max_length=30, serialize=False, editable=False, primary_key=True),
        ),
        migrations.DeleteModel(
            name='EventAttendance',
        ),
    ]
