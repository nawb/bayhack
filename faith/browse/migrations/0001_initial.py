# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link_Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(max_length=10)),
                ('link_id', models.IntegerField(max_length=10)),
                ('vote', models.IntegerField(default=0, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
