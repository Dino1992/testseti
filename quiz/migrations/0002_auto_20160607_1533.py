# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-07 15:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='theme',
            new_name='name',
        ),
    ]
