# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0025_auto_20170113_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full option name & details (e.g. open to whom, if early bird, etc.)', unique=True, max_length=400)),
                ('public', models.BooleanField(default=True, help_text=b'De-select this option to make this registration an internal use-only option')),
                ('cost', models.DecimalField(help_text=b'Include GST if required', max_digits=6, decimal_places=2)),
                ('meeting', models.ForeignKey(help_text=b'Meeting this option is for', to='asa18.Meeting')),
            ],
            options={
                'verbose_name': 'event sign-up option',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='cost',
        ),
        migrations.AddField(
            model_name='attendee',
            name='email',
            field=models.EmailField(default='joe.bloggs@anu.edu.au', unique=True, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='family_name',
            field=models.CharField(default='Bloggs', help_text=b'Your family name', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='given_names',
            field=models.CharField(default='Joe P.', help_text=b'Your given name(s)', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='is_asa_member',
            field=models.BooleanField(default=True, help_text=b'Are you a current ASA member?'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='name_order',
            field=models.CharField(default=b'w', help_text=b'In which order should your names be rendered?', max_length=1, choices=[(b'w', b'GivenName FAMILYNAME'), (b'e', b'FAMILYNAME GivenName')]),
        ),
        migrations.AddField(
            model_name='regooption',
            name='available_to',
            field=multiselectfield.db.fields.MultiSelectField(default='', max_length=66, choices=[(b'undergrad', b'Undergraduate student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='academic_level',
            field=models.CharField(help_text=b'Please select your academic level/appointment', max_length=15, choices=[(b'undergrad', b'Undergraduate student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff')]),
        ),
        migrations.AlterField(
            model_name='news',
            name='meetings',
            field=models.ManyToManyField(help_text=b'Please select all meetings this news item pertains to', to='asa18.Meeting', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set([('attendee', 'meeting_rego')]),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='attendee',
            field=models.ForeignKey(to='asa18.Attendee'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='event_rego',
            field=models.ForeignKey(to='asa18.EventOption'),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('attendee', 'event_rego')]),
        ),
    ]
