# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0014_auto_20161201_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prize',
            name='citation',
            field=tinymce.models.HTMLField(help_text=b'Use this field to provide the award citation, as well as give some brief info about the winner', blank=True),
            preserve_default=True,
        ),
    ]
