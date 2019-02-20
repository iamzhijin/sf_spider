# Generated by Django 2.1.4 on 2019-01-18 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=30, verbose_name='项目名称')),
                ('describe', models.TextField(null=True, verbose_name='项目描述')),
                ('code', models.CharField(max_length=10, verbose_name='项目编码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='项目创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='项目更新时间')),
            ],
        ),
    ]
