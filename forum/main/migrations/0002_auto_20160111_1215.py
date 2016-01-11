# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
    ]
