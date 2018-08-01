# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0033_auto_20170125_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='meeting',
            field=models.ForeignKey(default=1, editable=False, to='asa18.Meeting'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registration',
            name='meeting_rego',
            field=models.ForeignKey(default=None, to='asa18.RegoOption', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set([('attendee', 'meeting')]),
        ),
    ]
