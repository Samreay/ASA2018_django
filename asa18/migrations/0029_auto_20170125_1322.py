# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0028_auto_20170124_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='academic_level',
            field=models.CharField(help_text=b'Please select your academic level/appointment. This is *required* to provide you the appropriate registration options', max_length=15, choices=[(b'undergrad', b'Undergraduate/honours student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff'), (b'other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='family_name',
            field=models.CharField(help_text=b'Your family name (i.e. by which your publications are referenced)', max_length=300),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='gender',
            field=models.CharField(help_text=b"Please select the gender you identify as, or 'Do not disclose' if you do not wish to provide this information", max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female'), (b'x', b'Intersex'), (b'o', b'Other'), (b'z', b'Do not disclose')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='institution',
            field=models.CharField(help_text=b'Please write the full name of your home institution (no abbreviations)', max_length=300),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='is_asa_member',
            field=models.BooleanField(default=False, help_text=b'Tick if you are a current ASA member'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='locs',
            field=models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_loc', null=True, to='asa18.Meeting'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='socs',
            field=models.ManyToManyField(help_text=b'Please select the meeting(s) this person is on the SOC for', related_name='meetings_soc', null=True, to='asa18.Meeting'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='years_since_phd',
            field=models.CharField(help_text=b"Please select how many years it has been since you were awarded your PhD, or 'Do not disclose' if you do not wish to provide this information", max_length=5, choices=[(b'0-3', b'0 - 3 years'), (b'3-6', b'3 - 6 years'), (b'6-10', b'6 - 10 years'), (b'10-15', b'10 - 15 years'), (b'15+', b'15+ years'), (b'NA', b'Not applicable'), (b'z', b'Do not disclose')]),
        ),
        migrations.AlterField(
            model_name='regooption',
            name='available_to',
            field=multiselectfield.db.fields.MultiSelectField(max_length=72, choices=[(b'undergrad', b'Undergraduate/honours student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff'), (b'other', b'Other')]),
        ),
    ]
