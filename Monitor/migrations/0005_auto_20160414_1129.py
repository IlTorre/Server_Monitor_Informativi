# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0004_auto_20160414_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visualizzatafrazione',
            old_name='comune',
            new_name='frazione',
        ),
        migrations.RenameField(
            model_name='visualizzatamonitor',
            old_name='comune',
            new_name='monitor',
        ),
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 9, 29, 20, 190192, tzinfo=utc)),
        ),
    ]
