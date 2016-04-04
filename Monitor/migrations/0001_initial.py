# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Monitor.models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import django.contrib.auth.models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Frazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
                ('comune', models.ForeignKey(to='Monitor.Comune')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
                ('descrizione', models.CharField(max_length=200)),
                ('via', models.CharField(max_length=30)),
                ('frazione_posizionamento', models.ForeignKey(to='Monitor.Frazione')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor_ultima_connessione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('agg', models.DateTimeField(default=django.utils.timezone.now)),
                ('monitor', models.ForeignKey(to='Monitor.Monitor')),
            ],
        ),
        migrations.CreateModel(
            name='Notizia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titolo', models.CharField(max_length=30)),
                ('descrizione', models.CharField(max_length=400)),
                ('immagine', models.ImageField(default=None, upload_to=Monitor.models.get_nome_immagine_notizia)),
                ('approvata', models.BooleanField(default=False)),
                ('data_inserimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_scadenza', models.DateTimeField(default=datetime.datetime(2016, 4, 19, 8, 43, 25, 513580, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Ultimo_agg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('agg', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Comune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comune', models.ForeignKey(to='Monitor.Comune')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Frazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comune', models.ForeignKey(to='Monitor.Frazione')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='Vis_in_Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comune', models.ForeignKey(to='Monitor.Monitor')),
                ('notizia', models.ForeignKey(to='Monitor.Notizia')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('foto_profilo', models.ImageField(default='default/no_profilo.jpg', upload_to=Monitor.models.get_nome_immagine_utente)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', blank=True, verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', blank=True, verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
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
