# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import Monitor.models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0002_auto_20160407_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 28, 19, 53, 50, 378918, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notizia',
            name='immagine',
            field=models.ImageField(default=None, upload_to=Monitor.models.get_nome_immagine_notizia, null=True),
        ),
    ]
