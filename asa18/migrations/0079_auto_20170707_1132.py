# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0078_auto_20170616_1726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'ordering': ('time_start', 'time_end', 'id_no', 'presenter', 'title')},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('time_start', 'title', 'time_end')},
        ),
        migrations.AddField(
            model_name='meeting',
            name='program_hardcopy',
            field=models.FileField(help_text=b'Upload a hardcopy of the program here for download', null=True, upload_to=b'prog/%Y/%m/%d/', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='presentation',
            unique_together=set([('meeting', 'type', 'id_no'), ('meeting', 'title', 'presenter')]),
        ),
    ]
