# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-05 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0079_auto_20170707_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoption',
            name='name',
            field=models.CharField(help_text=b'Full option name & details (e.g. open to whom, if early bird, etc.)', max_length=255),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='abbrv',
            field=models.CharField(help_text=b'Abbreviated meeting name - avoid changing this once set!', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='blurb',
            field=models.TextField(blank=True, help_text=b'*Short* blurb about meeting', max_length=400),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='name',
            field=models.CharField(help_text=b'Full meeting name', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='policy',
            name='name',
            field=models.CharField(help_text=b'Policy title', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='title',
            field=models.CharField(help_text=b'Presentation title', max_length=255),
        ),
        migrations.AlterField(
            model_name='regooption',
            name='name',
            field=models.CharField(help_text=b'Full option name & details (e.g. open to whom, if early bird, etc.)', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='name',
            field=models.CharField(help_text=b'Sponsor name', max_length=255, unique=True),
        ),
    ]
