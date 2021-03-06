# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-13 05:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0084_auto_20180313_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='phone',
            field=models.CharField(help_text=b'Please use international dialling code if registering from overseas', max_length=16, validators=[django.core.validators.RegexValidator(message=b'Please use international dialling code if registering from overseas', regex=b'^\\+?\\d{7,15}$')]),
        ),
    ]
