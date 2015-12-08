# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0004_auto_20151207_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbresults',
            name='intensity',
            field=models.CharField(max_length=100, default='empty'),
        ),
    ]
