# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import trydjango18.views


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0002_auto_20151118_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbexpupload',
            name='EXPupload',
            field=models.FileField(upload_to=trydjango18.views.PathMaker2),
        ),
        migrations.AlterField(
            model_name='dbpdbup',
            name='PDBup',
            field=models.FileField(upload_to=trydjango18.views.PathMaker2),
        ),
    ]
