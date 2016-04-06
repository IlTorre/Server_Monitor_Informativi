# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0002_auto_20160406_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 9, 19, 45, 888599, tzinfo=utc)),
        ),
    ]
