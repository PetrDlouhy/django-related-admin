# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160110_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(blank=True, to='main.Musician', on_delete=models.CASCADE, null=True),
        ),
        migrations.AlterField(
            model_name='musician',
            name='last_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='concert',
            name='main_performer',
            field=models.ForeignKey(to='main.Musician', on_delete=models.CASCADE),
        ),
    ]
