# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0053_auto_20170214_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=2)),
                ('is_paid', models.BooleanField(default=False)),
                ('attendee', models.ForeignKey(to='asa18.Attendee')),
            ],
            options={
                'ordering': ['attendee'],
            },
        ),
        migrations.AlterModelOptions(
            name='regooption',
            options={'ordering': ['closes', 'opens', 'cost'], 'verbose_name': 'registration option'},
        ),
        migrations.RemoveField(
            model_name='eventregistration',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='payment_obj',
            field=models.ForeignKey(default=None, to='asa18.Payment', null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='payment_obj',
            field=models.ForeignKey(default=None, to='asa18.Payment', null=True),
        ),
    ]
