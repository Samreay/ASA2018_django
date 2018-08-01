# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0058_remove_lineitem_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
