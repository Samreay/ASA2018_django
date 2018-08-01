# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asa18', '0068_auto_20170330_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventregistration',
            options={'ordering': ['event', 'event_option', 'attendee']},
        ),
        migrations.AlterField(
            model_name='attendee',
            name='years_since_phd',
            field=models.CharField(help_text=b"Please select how many years it has been since you were awarded your PhD, or 'Do not disclose' if you do not wish to provide this information", max_length=5, choices=[(b'0-3', b'0 - 3 years'), (b'3-6', b'3 - 6 years'), (b'6-10', b'6 - 10 years'), (b'10-15', b'10 - 15 years'), (b'15+', b'15+ years'), (b'NA', b'Not applicable/awarded'), (b'z', b'Do not disclose')]),
        ),
        migrations.AlterUniqueTogether(
            name='lineitem',
            unique_together=set([('attendee', 'meeting_rego', 'event_rego')]),
        ),
    ]
