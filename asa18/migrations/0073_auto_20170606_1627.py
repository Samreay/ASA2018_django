# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0072_presentation_id_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='location',
            field=models.CharField(help_text=b'Address or other simple location of the event (you can add more description, Google Maps etc. in the event description. You can wrap your description in link tags if you do want to link to Google Maps from here.', max_length=300, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='presentation',
            unique_together=set([('type', 'id_no'), ('meeting', 'title', 'presenter')]),
        ),
    ]
