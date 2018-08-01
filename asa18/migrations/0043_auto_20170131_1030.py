# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0042_auto_20170131_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoption',
            name='meeting',
        ),
        migrations.AddField(
            model_name='eventoption',
            name='event',
            field=models.ForeignKey(default=1, to='asa18.Event', help_text=b'Meeting this option is for'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(default=1, to='asa18.Event'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(default=b'rZMjyK2KMlJSyHqZuIgfe4Gw7Ae853', max_length=30, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='eventoption',
            name='public',
            field=models.BooleanField(default=True, help_text=b'De-select this option to make this event an internal use-only option'),
        ),
    ]
