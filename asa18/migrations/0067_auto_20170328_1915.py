# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0066_attendee_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='prize',
            name='honoree_info',
            field=tinymce.models.HTMLField(help_text=b'Info about who the prize isnamed for', blank=True),
        ),
        migrations.AddField(
            model_name='prize',
            name='honoree_pic',
            field=models.ImageField(help_text=b'Roughly square photo', null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='prize',
            name='named_for',
            field=models.CharField(default=b'', help_text=b'Full name of honoree', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='phone',
            field=models.CharField(help_text=b'Please enter phone number in format +99999...', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?\\d{7,15}$', message=b'Please enter phone number in format +99999....')]),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='event_rego',
            field=models.OneToOneField(null=True, blank=True, to='asa18.EventRegistration'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='meeting_rego',
            field=models.OneToOneField(null=True, blank=True, to='asa18.Registration'),
        ),
    ]
