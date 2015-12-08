# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0005_dbresults_intensity'),
    ]

    operations = [
        migrations.CreateModel(
            name='dbrerun',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=10)),
                ('runNum', models.IntegerField(default=1)),
            ],
        ),
    ]
