# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models
from django.utils.timezone import utc
from django.conf import settings
import django.utils.timezone
import datetime
import Monitor.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comune',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Frazione',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(max_length=30)),
                ('comune', models.ForeignKey(to='Monitor.Comune')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(max_length=30)),
                ('descrizione', models.CharField(max_length=200)),
                ('via', models.CharField(max_length=30)),
                ('frazione_posizionamento', models.ForeignKey(to='Monitor.Frazione')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor_ultima_connessione',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('agg', models.DateTimeField(default=django.utils.timezone.now)),
                ('monitor', models.ForeignKey(to='Monitor.Monitor')),
            ],
        ),
        migrations.CreateModel(
            name='Notizia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('titolo', models.CharField(max_length=30)),
                ('descrizione', models.CharField(max_length=400)),
                ('immagine', models.ImageField(upload_to=Monitor.models.get_nome_immagine_notizia, default=None)),
                ('approvata', models.BooleanField(default=False)),
                ('data_inserimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_scadenza', models.DateTimeField(default=datetime.datetime(2016, 4, 21, 16, 5, 58, 663540, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Ultimo_agg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('agg', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Comune',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comune', models.ForeignKey(to='Monitor.Comune')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Frazione',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comune', models.ForeignKey(to='Monitor.Frazione')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Monitor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('comune', models.ForeignKey(to='Monitor.Monitor')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username')),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('foto_profilo', models.ImageField(upload_to=Monitor.models.get_nome_immagine_utente, default='/media/default/no_profilo.jpg')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='notizia',
            name='inserzionista',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
