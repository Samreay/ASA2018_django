# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0049_auto_20170131_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoption',
            name='dietary_required',
        ),
        migrations.AddField(
            model_name='event',
            name='dietary_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dietaryrestriction',
            name='restriction',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=12, choices=[(b'a', b'None'), (b'v', b'Vegetarian'), (b'vn', b'Vegan'), (b'g', b'Gluten-free'), (b'd', b'Dairy-free'), (b's', b'Seafood-free')]),
        ),
    ]
