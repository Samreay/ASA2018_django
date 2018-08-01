# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0067_auto_20170328_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='invoice_no',
            field=models.CharField(max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt_no',
            field=models.CharField(max_length=60, blank=True),
        ),
    ]
