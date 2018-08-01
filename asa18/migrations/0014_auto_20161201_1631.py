# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0013_auto_20161201_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prize',
            name='talk',
            field=models.ForeignKey(blank=True, to='asa18.Presentation', help_text=b'Add/attach the prize talk here', null=True),
            preserve_default=True,
        ),
    ]
