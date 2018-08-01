# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0022_auto_20161208_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-pub_date',), 'verbose_name': 'news item'},
        ),
        migrations.AlterModelOptions(
            name='policy',
            options={'ordering': ('name',), 'verbose_name_plural': 'policies'},
        ),
        migrations.AddField(
            model_name='prize',
            name='slug',
            field=models.SlugField(default='faulkner', help_text=b'Recommend you use auto-generated slug', unique=True, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policy',
            name='slug',
            field=models.SlugField(help_text=b'We recommend you use the auto-generated default for this field', max_length=100),
            preserve_default=True,
        ),
    ]
