# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorUltimaConnessione',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('agg', models.DateTimeField(default=django.utils.timezone.now)),
                ('monitor', models.ForeignKey(to='Monitor.Monitor')),
            ],
        ),
        migrations.RenameModel(
            old_name='Ultimo_agg',
            new_name='UltimoAggiornamento',
        ),
        migrations.RenameModel(
            old_name='Vis_in_Monitor',
            new_name='VisualizzataComune',
        ),
        migrations.RenameModel(
            old_name='Vis_in_Comune',
            new_name='VisualizzataFrazione',
        ),
        migrations.RenameModel(
            old_name='Vis_in_Frazione',
            new_name='VisualizzataMonitor',
        ),
        migrations.RemoveField(
            model_name='monitor_ultima_connessione',
            name='monitor',
        ),
        migrations.AlterField(
            model_name='notizia',
            name='data_scadenza',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 22, 9, 38, 11, 418370, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visualizzatacomune',
            name='comune',
            field=models.ForeignKey(to='Monitor.Comune'),
        ),
        migrations.AlterField(
            model_name='visualizzatafrazione',
            name='comune',
            field=models.ForeignKey(to='Monitor.Frazione'),
        ),
        migrations.AlterField(
            model_name='visualizzatamonitor',
            name='comune',
            field=models.ForeignKey(to='Monitor.Monitor'),
        ),
        migrations.DeleteModel(
            name='Monitor_ultima_connessione',
        ),
    ]
