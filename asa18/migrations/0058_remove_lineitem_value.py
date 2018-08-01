# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0057_payment_paid_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineitem',
            name='value',
        ),
    ]
