# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0047_auto_20170131_1146'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventoption',
            unique_together=set([('event', 'name')]),
        ),
    ]
