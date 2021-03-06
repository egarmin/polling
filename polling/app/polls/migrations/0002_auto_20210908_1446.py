# Generated by Django 2.2.10 on 2021-09-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='questions',
            field=models.ManyToManyField(related_name='polls', to='polls.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='typ',
            field=models.CharField(choices=[('txt', 'Your text'), ('simple', 'The one option'), ('multi', 'Several options')], max_length=16),
        ),
    ]
