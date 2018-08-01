# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0075_auto_20170607_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='extended_description',
            field=tinymce.models.HTMLField(help_text=b'Use this field if a longer description is required, e.g. for a special lunch', blank=True),
        ),
    ]
