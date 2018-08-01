# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0059_registration_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
