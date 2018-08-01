# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0016_auto_20161201_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='asa-2017-conference-dinner', help_text=b'Recommend you use auto-generated value', unique=True, max_length=100),
            preserve_default=False,
        ),
    ]
