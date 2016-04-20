# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0005_auto_20160414_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 5, 13, 6, 47, 411064, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notizia',
            name='descrizione',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='notizia',
            name='titolo',
            field=models.CharField(max_length=40),
        ),
    ]
