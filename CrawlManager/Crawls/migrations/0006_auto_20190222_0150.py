# Generated by Django 2.1.4 on 2019-02-22 01:50

import Crawls.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawls', '0005_auto_20190215_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawls',
            name='code',
            field=models.CharField(max_length=50, null=True, verbose_name='爬虫编码'),
        ),
        migrations.AlterField(
            model_name='crawls',
            name='crawl_file',
            field=models.FileField(max_length=50, upload_to=Crawls.models.upload_to, verbose_name='爬虫文件'),
        ),
    ]
