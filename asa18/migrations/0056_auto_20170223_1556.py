# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0055_auto_20170223_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('order_id', models.CharField(max_length=70, serialize=False, editable=False, primary_key=True)),
                ('cost', models.DecimalField(null=True, max_digits=6, decimal_places=2)),
                ('is_paid', models.BooleanField(default=False, editable=False)),
                ('invoice_no', models.CharField(unique=True, max_length=60, editable=False, blank=True)),
                ('receipt_no', models.CharField(unique=True, max_length=60, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attendee', models.ForeignKey(to='asa18.Attendee')),
            ],
        ),
        migrations.AddField(
            model_name='lineitem',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 23, 15, 56, 59, 506127), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='event_rego',
            field=models.ForeignKey(to='asa18.EventRegistration', null=True),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='meeting_rego',
            field=models.ForeignKey(to='asa18.Registration', null=True),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='payment',
            field=models.ForeignKey(default=None, to='asa18.Payment', null=True),
        ),
    ]
