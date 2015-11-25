# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dbEXPupload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=40)),
                ('EXPupload', models.FileField(upload_to='Storage/%Y/%m/%d', blank=True, null=True, verbose_name='Upload locally')),
            ],
        ),
        migrations.CreateModel(
            name='dbPara',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=40)),
                ('turns', models.FloatField(default='5')),
                ('units', models.FloatField(default='5')),
                ('rise', models.FloatField(default='5')),
            ],
        ),
        migrations.CreateModel(
            name='dbPDBdown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=40)),
                ('PDBdown', models.CharField(validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 4', regex='^.{4}$')], blank=True, null=True, max_length=4, verbose_name='Enter a 4-digit PDB code')),
            ],
        ),
        migrations.CreateModel(
            name='dbPDBup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=40)),
                ('PDBup', models.FileField(upload_to='Storage/%Y/%m/%d', blank=True, null=True, verbose_name='Upload locally')),
            ],
        ),
        migrations.CreateModel(
            name='dbResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(blank=True, null=True, max_length=40)),
                ('output', models.FileField(upload_to='Storage/%Y/%m/%d', blank=True, null=True)),
                ('chisq', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
