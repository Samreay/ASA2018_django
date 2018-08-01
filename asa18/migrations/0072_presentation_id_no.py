# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0071_auto_20170606_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='id_no',
            field=models.IntegerField(help_text=b'Leave blank to not use ID number. IDs will be displayed as XNNN, where X is the presentation type (e.g. T for talk, P for poster, etc.)', null=True, blank=True),
        ),
    ]
