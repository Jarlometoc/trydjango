# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0003_auto_20151119_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbresults',
            name='R_step',
            field=models.FloatField(default=0.001),
        ),
        migrations.AddField(
            model_name='dbresults',
            name='layer_lines',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='dbresults',
            name='gridPhi',
            field=models.IntegerField(default=128),
        ),
        migrations.AlterField(
            model_name='dbresults',
            name='gridR',
            field=models.IntegerField(default=256),
        ),
        migrations.AlterField(
            model_name='dbresults',
            name='gridZ',
            field=models.IntegerField(default=128),
        ),
    ]
