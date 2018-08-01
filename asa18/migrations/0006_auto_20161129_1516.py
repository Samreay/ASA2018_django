# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0005_auto_20161129_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='meetings',
            field=models.ManyToManyField(help_text=b'Please select all meetings this news item pertains to', to='asa18.Meeting', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(help_text=b'Recommend leaving this as the auto-generated default', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ImageField(help_text=b'Upload a sponsor logo here - the closer to square the image is, the better. No larger than 500px should be necessary.', upload_to=b''),
            preserve_default=True,
        ),
    ]
