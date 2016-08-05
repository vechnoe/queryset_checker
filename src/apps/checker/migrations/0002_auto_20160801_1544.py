# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-01 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queryexception',
            name='query',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exception', to='checker.Query', verbose_name='Query set'),
        ),
        migrations.AlterField(
            model_name='result',
            name='query',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='checker.Query', verbose_name='Query set'),
        ),
    ]
