# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0046_auto_20170131_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoption',
            name='name',
            field=models.CharField(help_text=b'Full option name & details (e.g. open to whom, if early bird, etc.)', max_length=400),
        ),
    ]
