# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0060_eventregistration_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='receipt_no',
            field=models.CharField(max_length=60, editable=False, blank=True),
        ),
    ]
