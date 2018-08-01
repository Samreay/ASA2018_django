# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0063_auto_20170315_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paid_amount',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True),
        ),
    ]
