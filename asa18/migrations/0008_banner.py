# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0007_regooption_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(help_text=b'Should be an image 5120x600 at minimum, with the most interesting content centered vertically', upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
