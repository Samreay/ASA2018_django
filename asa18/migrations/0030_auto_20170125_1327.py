# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0029_auto_20170125_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='family_name',
            field=models.CharField(help_text=b'Your family name (i.e. by which your publications are referenced)', max_length=50),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='given_names',
            field=models.CharField(help_text=b'Your given name(s)', max_length=100),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='institution',
            field=models.CharField(help_text=b'Please write the full name of your home institution (no abbreviations)', max_length=100),
        ),
    ]
