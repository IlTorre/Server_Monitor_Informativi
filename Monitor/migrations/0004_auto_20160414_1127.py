# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import Monitor.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0003_auto_20160413_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 9, 27, 37, 749272, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notizia',
            name='immagine',
            field=models.ImageField(upload_to=Monitor.models.get_nome_immagine_notizia, default=None),
        ),
    ]
