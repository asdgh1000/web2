# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20161020_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloginfo',
            name='abstract',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='bloginfo',
            name='cover_img',
            field=models.CharField(default='default.png', max_length=255),
        ),
    ]
