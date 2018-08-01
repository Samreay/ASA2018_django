# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0006_auto_20161129_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='regooption',
            name='public',
            field=models.BooleanField(default=True, help_text=b'De-select this option to make this registration an internal use-only option'),
            preserve_default=True,
        ),
    ]
