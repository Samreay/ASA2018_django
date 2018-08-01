# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0062_auto_20170315_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='event_rego',
            field=models.OneToOneField(null=True, to='asa18.EventRegistration'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='meeting_rego',
            field=models.OneToOneField(null=True, to='asa18.Registration'),
        ),
    ]
