# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0051_auto_20170206_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='abstract_date',
            field=models.DateTimeField(help_text=b'What is the end datetime for accepting abstracts? (Note this is distinct from registration dates)', null=True, blank=True),
        ),
    ]
