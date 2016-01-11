# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160111_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
