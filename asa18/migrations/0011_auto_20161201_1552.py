# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0010_remove_banner_horz_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full name, as it will appear in the conference program', max_length=300)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('institution', models.CharField(help_text=b'Please write the full name of your home institution (no abbreviations', max_length=300)),
                ('academic_level', models.CharField(help_text=b'Please select your academic level/appointment', max_length=15, choices=[(b'undergrad', b'Undergraduate student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff')])),
                ('gender', models.CharField(blank=True, help_text=b"Please select the gender you identify as, or 'Do not disclose' if you do not wish to provide this information", max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female'), (b'x', b'Intersex'), (b'o', b'Other'), (b'z', b'Do not disclose')])),
                ('years_since_phd', models.CharField(default=b'', help_text=b'Please select how many years it has been since you were awarded your PhD', max_length=5, choices=[(b'0-3', b'0 - 3 years'), (b'3-6', b'3 - 6 years'), (b'6-10', b'6 - 10 years'), (b'10-15', b'10 - 15 years'), (b'15+', b'15+ years'), (b'NA', b'Not applicable'), (b'z', b'Do not disclose')])),
                ('is_organizer', models.BooleanField(default=False, help_text=b'Is this person a conference organizer?')),
                ('locs', models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_loc', to='asa18.Meeting', blank=True)),
                ('socs', models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_soc', to='asa18.Meeting', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Event name', max_length=200)),
                ('rego_required', models.BooleanField(default=False, help_text=b'Is registration required to attend this event?')),
                ('cost', models.DecimalField(help_text=b'Include GST if required; leave blank if event is free', null=True, max_digits=6, decimal_places=2, blank=True)),
                ('description', tinymce.models.HTMLField()),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('meetings', models.ManyToManyField(help_text=b'Select all meetings this event is attached to', to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('attendee', models.ForeignKey(to='asa18.Attendee')),
                ('event', models.ForeignKey(to='asa18.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Presentation title', max_length=400)),
                ('abstract', tinymce.models.HTMLField(help_text=b'Abstract - LaTeX allowed?')),
                ('type', models.CharField(default=b't', max_length=1, choices=[(b't', b'Talk'), (b'i', b'Invited talk'), (b'p', b'Poster')])),
                ('status', models.CharField(default=b's', max_length=1, choices=[(b's', b'Submitted')])),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('meeting', models.ForeignKey(help_text=b'This is the meeting the presentation is submitted for, *not* the assigned meeting - that is read from the linked Session object', to='asa18.Meeting')),
                ('presenter', models.ForeignKey(to='asa18.Attendee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Prize name', max_length=200)),
                ('about', tinymce.models.HTMLField(help_text=b'About the prize')),
                ('citation', tinymce.models.HTMLField(help_text=b'Use this field to provide the award citation, as well as give some brief info about the winner')),
                ('awardee', models.ForeignKey(blank=True, to='asa18.Attendee', help_text=b'Leave blank to just advertise the prize - attach an attendee when you want to make the announcement')),
                ('meeting', models.ForeignKey(to='asa18.Meeting')),
                ('talk', models.ForeignKey(blank=True, to='asa18.Presentation', help_text=b'Add/attach the prize talk here')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('attendee', models.ForeignKey(to='asa18.Attendee')),
                ('meeting_rego', models.ForeignKey(to='asa18.RegoOption')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Session title', max_length=200)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('chair', models.ForeignKey(to='asa18.Attendee')),
                ('meeting', models.ForeignKey(to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='presentation',
            name='session',
            field=models.ForeignKey(to='asa18.Session', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='distinct_color',
            field=colorfield.fields.ColorField(default=b'#000000', help_text=b'Choose a distinctive colour to differentiate this meeting from others. It should *not* be red or red-like, and should be an appropriate colour for having white text laid over it.', max_length=10),
            preserve_default=True,
        ),
    ]
