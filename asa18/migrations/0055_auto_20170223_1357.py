# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0054_auto_20170222_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=2)),
                ('attendee', models.ForeignKey(to='asa18.Attendee')),
            ],
            options={
                'ordering': ['attendee'],
            },
        ),
        migrations.RemoveField(
            model_name='payment',
            name='attendee',
        ),
        migrations.RemoveField(
            model_name='eventregistration',
            name='payment_obj',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='payment_obj',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
