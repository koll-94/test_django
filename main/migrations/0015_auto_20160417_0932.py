# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-17 09:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20160417_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docfield',
            old_name='doc_str',
            new_name='docstructure',
        ),
        migrations.RenameField(
            model_name='docstructure',
            old_name='doc_type',
            new_name='doctype',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='sub_type',
            new_name='docsubtype',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='doc_type',
            new_name='doctype',
        ),
    ]
