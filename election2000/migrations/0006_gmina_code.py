# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election2000', '0005_circuit'),
    ]

    operations = [
        migrations.AddField(
            model_name='gmina',
            name='code',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
