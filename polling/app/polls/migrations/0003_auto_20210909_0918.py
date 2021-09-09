# Generated by Django 2.2.10 on 2021-09-09 09:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210908_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='data',
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
