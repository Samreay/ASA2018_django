# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0064_payment_paid_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='payment',
            field=models.ForeignKey(default=None, to='asa18.Payment'),
        ),
    ]
