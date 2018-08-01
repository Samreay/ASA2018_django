# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0040_auto_20170131_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.CharField(default=b'ih0GNnQcSMUPsKGNuLH9Z5vVlTtXq0', max_length=30, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterUniqueTogether(
            name='presentation',
            unique_together=set([('meeting', 'title', 'presenter')]),
        ),
    ]
