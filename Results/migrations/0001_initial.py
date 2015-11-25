# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dbResults',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=10)),
                ('PDBused', models.CharField(max_length=100)),
                ('experimentalData', models.CharField(max_length=100)),
                ('turns', models.FloatField(default=5)),
                ('units', models.FloatField(default=27)),
                ('rise', models.FloatField(default=2.9)),
                ('rescutL', models.FloatField(default=0.0833333333)),
                ('rescutH', models.FloatField(default=0.3333333333)),
                ('LorR', models.CharField(max_length=1, default='R')),
                ('rfactor', models.CharField(max_length=5, default='False')),
                ('bfactor', models.FloatField(default=20.0)),
                ('bfactorSolv', models.FloatField(default=400)),
                ('bfactorSolvK', models.FloatField(default=0.4)),
                ('qfhtK1', models.FloatField(default=2.0)),
                ('qfhtK2', models.FloatField(default=2.2)),
                ('scscaling', models.FloatField(default=0.92)),
                ('gridR', models.FloatField(default=256)),
                ('gridZ', models.FloatField(default=128)),
                ('gridPhi', models.FloatField(default=128)),
                ('fibrilPDB', models.CharField(max_length=100, default='empty')),
                ('LLoutput', models.CharField(max_length=100, default='empty')),
                ('LLoutputPic', models.CharField(max_length=100, default='Storage/bunny.jpg')),
                ('FlagFile', models.CharField(max_length=100, default='empty')),
                ('denovo', models.CharField(max_length=100, default='empty')),
                ('Score', models.CharField(max_length=100, default='empty')),
                ('chisq', models.FloatField(default=0)),
            ],
        ),
    ]
