# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0030_auto_20170125_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='locs',
            field=models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_loc', to='asa18.Meeting', blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='socs',
            field=models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_soc', to='asa18.Meeting', blank=True),
        ),
    ]
