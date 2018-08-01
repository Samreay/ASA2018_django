# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0039_auto_20170130_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(default=b'ta05H3UpjxUF3iN15EwWmkIKnuQ6o5', max_length=30, serialize=False, editable=False, primary_key=True),
        ),
    ]
