# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150509_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='large',
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 23, 50, 7, 423768, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
