# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-15 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('blog_name', models.CharField(blank=True, max_length=50)),
                ('blog_text', models.CharField(blank=True, max_length=2000)),
            ],
            options={
                'db_table': 'blog',
                'managed': False,
            },
        ),
    ]