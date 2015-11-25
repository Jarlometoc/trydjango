# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbresults',
            name='jobname',
            field=models.CharField(max_length=50, default='none choseN'),
            preserve_default=False,
        ),
    ]
