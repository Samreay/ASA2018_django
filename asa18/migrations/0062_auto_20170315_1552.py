# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0061_auto_20170315_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='invoice_no',
            field=models.CharField(max_length=60, editable=False, blank=True),
        ),
    ]
