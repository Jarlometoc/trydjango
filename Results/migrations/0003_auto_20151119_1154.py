# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0002_dbresults_jobname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbresults',
            name='FlagFile',
        ),
        migrations.RemoveField(
            model_name='dbresults',
            name='LLoutput',
        ),
        migrations.RemoveField(
            model_name='dbresults',
            name='Score',
        ),
        migrations.RemoveField(
            model_name='dbresults',
            name='denovo',
        ),
    ]
