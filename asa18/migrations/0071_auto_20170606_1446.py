# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0070_auto_20170502_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('time_start', 'time_end', 'title')},
        ),
        migrations.AlterField(
            model_name='attendee',
            name='state',
            field=models.CharField(default=b'x', max_length=1, choices=[(b'a', b'ACT'), (b'n', b'NSW'), (b't', b'NT'), (b'q', b'QLD'), (b's', b'SA'), (b'h', b'TAS'), (b'v', b'VIC'), (b'w', b'WA'), (b'x', b'N/A')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='rego_closes',
            field=models.DateTimeField(help_text=b'Leave blank to use the rego opening date of the related event(s)', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('meeting', 'time_start', 'time_end', 'title')]),
        ),
    ]
