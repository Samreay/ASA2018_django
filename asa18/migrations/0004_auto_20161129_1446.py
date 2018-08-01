# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0003_auto_20161129_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='slug',
            field=models.SlugField(max_length=100),
            preserve_default=True,
        ),
    ]
