# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0052_meeting_abstract_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dietaryrestriction',
            name='restriction',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=10, choices=[(b'v', b'Vegetarian'), (b'vn', b'Vegan'), (b'g', b'Gluten-free'), (b'd', b'Dairy-free'), (b's', b'Seafood-free')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='abstract_date',
            field=models.DateTimeField(help_text=b'What is the end datetime for accepting abstracts? Leave blank to enforce no date. (Note this is distinct from registration dates)', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('attendee', 'event')]),
        ),
    ]
