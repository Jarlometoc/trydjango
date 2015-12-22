# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0006_dbrerun'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbresults',
            name='mostRes',
            field=models.IntegerField(default=0),
        ),
    ]
