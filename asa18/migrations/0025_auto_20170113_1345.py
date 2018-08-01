# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asa18', '0024_auto_20170113_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='name',
        ),
        migrations.AddField(
            model_name='attendee',
            name='user',
            field=models.OneToOneField(default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='academic_level',
            field=models.CharField(help_text=b'Please select your academic level/appointment', max_length=15, choices=[(b'undergrad', b'Undergraduate student'), (b'masters', b'Masters student'), (b'phd', b'PhD student'), (b'postdoc', b'Postdoctoral Fellow'), (b'fellow', b'Research Fellow'), (b'faculty', b'Faculty'), (b'emeritus', b'Emeritus faculty'), (b'professional', b'Professional staff'), (b'o', b'Other')]),
        ),
    ]
