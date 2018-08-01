# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0008_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='horz_position',
            field=models.DecimalField(decimal_places=1, default=None, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], max_digits=4, blank=True, help_text=b'Set percentage value here for horizontal positioning of banner image. Leave blank to use default (50).', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='banner',
            name='vert_position',
            field=models.DecimalField(decimal_places=1, default=None, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], max_digits=4, blank=True, help_text=b'Set percentage value here for vertical positioning of banner image. Leave blank to use default (50).', null=True),
            preserve_default=True,
        ),
    ]
