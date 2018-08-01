# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0045_auto_20170131_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(max_length=30, serialize=False, editable=False, primary_key=True),
        ),
    ]
