# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0050_auto_20170131_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='address',
            field=models.CharField(default=b'', help_text=b'Required for invoicing', max_length=300),
        ),
        migrations.AddField(
            model_name='attendee',
            name='country',
            field=django_countries.fields.CountryField(default='AUS', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='phone',
            field=models.CharField(default='', help_text=b'Please enter phone number in format +99999...', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?\\d{8,15}$', message=b'Please enter phone number in format +99999....')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='postcode',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AddField(
            model_name='attendee',
            name='state',
            field=models.CharField(default=b'x', max_length=1, choices=[(b'a', b'ACT'), (b'n', b'NSW'), (b't', b'NT'), (b'q', b'QLD'), (b's', b'SA'), (b's', b'TAS'), (b'v', b'VIC'), (b'w', b'WA'), (b'x', b'N/A')]),
        ),
    ]
