# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0019_remove_event_rego_opens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publication_date',
            field=models.DateTimeField(help_text=b'Time this event should be made publically available for viewing. Note this does *not* affect registrations.'),
            preserve_default=True,
        ),
    ]
