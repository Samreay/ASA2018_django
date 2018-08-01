# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full meeting name', unique=True, max_length=400)),
                ('abbrv', models.CharField(help_text=b'Abbreviated meeting name - avoid changing this once set!', unique=True, max_length=400)),
                ('date_start', models.DateField(help_text=b'First day of meeting')),
                ('date_end', models.DateField(help_text=b'Last day of meeting (leave blank for a single-day meeting)', blank=True)),
                ('blurb', models.CharField(help_text=b'*Short* blurb about meeting', max_length=400, blank=True)),
                ('description', tinymce.models.HTMLField(help_text=b'Detailed description of meeting - you can include sections covering all manner of things, and load in images/Google maps frames etc.')),
                ('distinct_color', colorfield.fields.ColorField(default=b'#000000', help_text=b'Choose a distinctive colour to differentiate this meeting from others', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField()),
                ('body', tinymce.models.HTMLField()),
                ('pub_date', models.DateTimeField(help_text=b'You can back-date or future-date news items to have them appear earlier on the site, or have them be released at a particular time', null=True, blank=True)),
                ('meetings', models.ManyToManyField(help_text=b'Please select all meetings this news item pertains to', to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Policy title', unique=True, max_length=400)),
                ('content', tinymce.models.HTMLField(help_text=b'Policy content')),
                ('meetings', models.ManyToManyField(help_text=b'Please select all meetings this policy applies to', to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegoOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full option name & details (e.g. open to whom, if early bird, etc.)', unique=True, max_length=400)),
                ('cost', models.DecimalField(help_text=b'Include GST if required', max_digits=6, decimal_places=2)),
                ('opens', models.DateTimeField(help_text=b'Local time to open rego option')),
                ('closes', models.DateTimeField(help_text=b'Local time to close option')),
                ('meeting', models.ForeignKey(help_text=b'Meeting this option is for', to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Sponsor name', unique=True, max_length=300)),
                ('url', models.URLField(help_text=b'Sponsor website')),
                ('logo', models.ImageField(help_text=b'Upload a sponsor logo here - the closer to square the image is, the better', upload_to=b'')),
                ('meetings', models.ManyToManyField(to='asa18.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
