# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-04 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0002_auto_20160801_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='query',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='checker.Query'),
        ),
    ]
