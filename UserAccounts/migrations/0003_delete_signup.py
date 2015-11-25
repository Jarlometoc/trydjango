# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccounts', '0002_auto_20150902_1014'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SignUp',
        ),
    ]
