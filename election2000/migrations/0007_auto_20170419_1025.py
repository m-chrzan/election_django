# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 10:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election2000', '0006_gmina_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together=set([('first_name', 'last_name')]),
        ),
    ]
