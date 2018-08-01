# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0056_auto_20170223_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(null=True),
        ),
    ]
