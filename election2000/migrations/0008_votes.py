# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election2000', '0007_auto_20170419_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election2000.Candidate')),
                ('circuit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election2000.Circuit')),
            ],
        ),
    ]