# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0077_auto_20170607_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dietaryrestriction',
            options={'ordering': ('event_rego__attendee', 'event_rego__event')},
        ),
        migrations.AlterModelOptions(
            name='presentation',
            options={'ordering': ('time_start', 'time_end', 'id', 'presenter', 'title')},
        ),
        migrations.AlterField(
            model_name='presentation',
            name='status',
            field=models.CharField(default=b's', max_length=1, choices=[(b's', b'Submitted'), (b'a', b'Accepted'), (b'd', b'Demoted'), (b'r', b'Rejected'), (b'w', b'Withdrawn')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='chair',
            field=models.ForeignKey(blank=True, to='asa18.Attendee', null=True),
        ),
    ]
