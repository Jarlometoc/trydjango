# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0002_auto_20151125_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbpara2',
            name='gridPhi',
            field=models.IntegerField(default=128),
        ),
        migrations.AlterField(
            model_name='dbpara2',
            name='gridR',
            field=models.IntegerField(default=256),
        ),
        migrations.AlterField(
            model_name='dbpara2',
            name='gridZ',
            field=models.IntegerField(default=128),
        ),
    ]
