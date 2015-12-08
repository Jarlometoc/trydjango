# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0003_auto_20151130_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbpara2',
            name='R_step',
            field=models.FloatField(default=0.001),
        ),
        migrations.AddField(
            model_name='dbpara2',
            name='layer_lines',
            field=models.IntegerField(default=20),
        ),
    ]
