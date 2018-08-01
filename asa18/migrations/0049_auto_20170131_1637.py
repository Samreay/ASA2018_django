# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0048_auto_20170131_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dietaryrestriction',
            name='restriction',
            field=multiselectfield.db.fields.MultiSelectField(max_length=14, choices=[(b'a', b'None'), (b'v', b'Vegetarian'), (b'vn', b'Vegan'), (b'g', b'Gluten-free'), (b'd', b'Dairy-free'), (b's', b'Seafood-free'), (b'o', b'Other')]),
        ),
    ]
