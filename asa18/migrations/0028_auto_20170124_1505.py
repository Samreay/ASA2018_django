# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0027_remove_event_rego_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryRestriction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restriction', models.CharField(default=b'a', max_length=2, choices=[(b'a', b'None'), (b'v', b'Vegetarian'), (b'vn', b'Vegan'), (b'g', b'Gluten-free'), (b'd', b'Dairy-free'), (b's', b'Seafood-free'), (b'o', b'Other')])),
                ('other_restriction', models.CharField(default=b'', max_length=200, blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='eventregistration',
            old_name='event_rego',
            new_name='event_option',
        ),
        migrations.AddField(
            model_name='eventoption',
            name='extra_guests',
            field=models.IntegerField(default=0, help_text=b'How many extra guests this event option includes'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='dietary_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='extra_comments',
            field=models.CharField(default=b'', help_text=b'Please add any extra comments regarding your registration here', max_length=300, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('attendee', 'event_option')]),
        ),
        migrations.AddField(
            model_name='dietaryrestriction',
            name='event_rego',
            field=models.ForeignKey(to='asa18.EventRegistration'),
        ),
    ]
