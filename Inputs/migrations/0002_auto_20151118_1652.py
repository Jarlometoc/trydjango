# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import trydjango18.views


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dbPara2',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=10)),
                ('rfactor', models.CharField(default='False', max_length=5)),
                ('bfactor', models.FloatField(default=20)),
                ('bfactorSolv', models.FloatField(default=400)),
                ('bfactorSolvK', models.FloatField(default=0.4)),
                ('qfhtK1', models.FloatField(default=2.0)),
                ('qfhtK2', models.FloatField(default=2.2)),
                ('scscaling', models.FloatField(default=0.92)),
                ('gridR', models.FloatField(default=256)),
                ('gridZ', models.FloatField(default=127)),
                ('gridPhi', models.FloatField(default=129)),
            ],
        ),
        migrations.DeleteModel(
            name='dbResults',
        ),
        migrations.AddField(
            model_name='dbpara',
            name='LorR',
            field=models.CharField(default='R', max_length=1),
        ),
        migrations.AddField(
            model_name='dbpara',
            name='jobname',
            field=models.CharField(default=' ', max_length=50),
        ),
        migrations.AddField(
            model_name='dbpara',
            name='rescutH',
            field=models.FloatField(default=0.333333333),
        ),
        migrations.AddField(
            model_name='dbpara',
            name='rescutL',
            field=models.FloatField(default=0.0833333333),
        ),
        migrations.AlterField(
            model_name='dbexpupload',
            name='EXPupload',
            field=models.FileField(default='none choseN', upload_to=trydjango18.views.PathMaker),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dbexpupload',
            name='username',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dbpara',
            name='rise',
            field=models.FloatField(default=2.9),
        ),
        migrations.AlterField(
            model_name='dbpara',
            name='turns',
            field=models.FloatField(default=27),
        ),
        migrations.AlterField(
            model_name='dbpara',
            name='units',
            field=models.FloatField(default=5),
        ),
        migrations.AlterField(
            model_name='dbpara',
            name='username',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dbpdbdown',
            name='PDBdown',
            field=models.CharField(default='none choseN', validators=[django.core.validators.RegexValidator(message='Length has to be 4', regex='^.{4}$', code='nomatch')], max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dbpdbdown',
            name='username',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dbpdbup',
            name='PDBup',
            field=models.FileField(default='none choseN', upload_to=trydjango18.views.PathMaker),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dbpdbup',
            name='username',
            field=models.CharField(max_length=10),
        ),
    ]
