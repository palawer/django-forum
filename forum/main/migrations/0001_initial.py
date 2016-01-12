# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('topics', models.PositiveIntegerField(default=0)),
                ('posts', models.PositiveIntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('category', models.ForeignKey(to='main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('content', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('forum', models.ForeignKey(to='main.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posts', models.PositiveIntegerField(default=0)),
                ('timezone', models.FloatField(default=0)),
                ('avatar', models.CharField(max_length=100)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=10)),
                ('website', models.URLField()),
                ('location', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('views', models.PositiveIntegerField(default=0)),
                ('replies', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('first_post', models.ForeignKey(related_name='first_topic_post', to='main.Post')),
                ('forum', models.ForeignKey(to='main.Forum')),
                ('last_post', models.ForeignKey(related_name='last_topic_post', to='main.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(to='main.Topic'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.ForeignKey(related_name='last_forum_post', blank=True, to='main.Post', null=True),
        ),
    ]
