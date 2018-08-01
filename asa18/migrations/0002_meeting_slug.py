# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='slug',
            field=models.SlugField(default='asa-2017', help_text=b'URL root for this meeting - often best to use the default that is auto-generated from the abbreviation', unique=True),
            preserve_default=False,
        ),
    ]
