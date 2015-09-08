# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signup',
            old_name='uppdated',
            new_name='updated',
        ),
        migrations.AlterField(
            model_name='signup',
            name='full_name',
            field=models.CharField(null=True, max_length=120),
        ),
    ]
