# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0043_auto_20170131_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventregistration',
            name='dietary_required',
        ),
        migrations.AddField(
            model_name='eventoption',
            name='dietary_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(default=b'ykUWvFoI2XhEElkNEyqZVMBGALXtrH', max_length=30, serialize=False, editable=False, primary_key=True),
        ),
    ]
