# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0002_meeting_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'news item'},
        ),
        migrations.AlterModelOptions(
            name='policy',
            options={'verbose_name_plural': 'policies'},
        ),
        migrations.AlterModelOptions(
            name='regooption',
            options={'verbose_name': 'registration option'},
        ),
        migrations.AddField(
            model_name='policy',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]
