# Generated by Django 2.1 on 2019-10-05 15:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('blog', '0002_auto_20191005_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 5, 15, 58, 16, 994076, tzinfo=utc)),
        ),
    ]