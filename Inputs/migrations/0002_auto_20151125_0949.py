# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import trydjango18.views
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dbPara2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=10)),
                ('rfactor', models.CharField(max_length=5, default='False')),
                ('bfactor', models.FloatField(default=20)),
                ('bfactorSolv', models.FloatField(default=400)),
                ('bfactorSolvK', models.FloatField(default=0.4)),
                ('qfhtK1', models.FloatField(default=2.0)),
                ('qfhtK2', models.FloatField(default=2.2)),
                ('scscaling', models.FloatField(default=0.92)),
                ('gridR', models.FloatField(default=256)),
                ('gridZ', models.FloatField(default=128)),
                ('gridPhi', models.FloatField(default=128)),
            ],
        ),
        migrations.DeleteModel(
            name='dbResults',
        ),
        migrations.AddField(
            model_name='dbpara',
            name='LorR',
            field=models.CharField(max_length=1, default='R'),
        ),
        migrations.AddField(
            model_name='dbpara',
            name='jobname',
            field=models.CharField(max_length=50, default=' '),
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
            field=models.FileField(default='none choseN', upload_to=trydjango18.views.PathMaker2),
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
            field=models.CharField(max_length=4, default='none choseN', validators=[django.core.validators.RegexValidator(regex='^.{4}$', code='nomatch', message='Length has to be 4')]),
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
            field=models.FileField(default='none choseN', upload_to=trydjango18.views.PathMaker2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dbpdbup',
            name='username',
            field=models.CharField(max_length=10),
        ),
    ]
