# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0035_auto_20170127_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registration',
            options={'ordering': ['attendee', 'meeting']},
        ),
        migrations.AddField(
            model_name='meeting',
            name='accept_abstracts',
            field=models.BooleanField(default=True, help_text=b'Does this meeting accept abstracts from public registrations?'),
        ),
    ]
