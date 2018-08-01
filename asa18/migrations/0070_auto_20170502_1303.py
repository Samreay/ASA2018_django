# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0069_auto_20170501_1654'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lineitem',
            unique_together=set([('attendee', 'event_rego'), ('attendee', 'meeting_rego')]),
        ),
    ]
