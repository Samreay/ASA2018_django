# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0012_auto_20161201_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prize',
            name='awardee',
            field=models.ForeignKey(blank=True, to='asa18.Attendee', help_text=b'Leave blank to just advertise the prize - attach an attendee when you want to make the announcement', null=True),
            preserve_default=True,
        ),
    ]
