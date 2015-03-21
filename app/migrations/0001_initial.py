# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Untitled', max_length=256)),
                ('description', models.CharField(max_length=10000, null=True, blank=True)),
                ('author', models.CharField(default=b'Anonymous', max_length=256)),
                ('large', models.BooleanField(default=False)),
                ('full_width', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 3, 21, 0, 32, 11, 996468, tzinfo=utc))),
                ('cover_photo', models.ForeignKey(blank=True, to='app.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
