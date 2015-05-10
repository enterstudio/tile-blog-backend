# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sub_photos',
            field=models.ManyToManyField(related_name='image_sub', null=True, to='app.Image', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 9, 1, 27, 56, 652273, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
