# Generated by Django 4.0 on 2022-05-27 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DesignBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True, verbose_name='版本')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='版本名称')),
                ('code', models.TextField(null=True, verbose_name='源代码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '设计数据备份',
                'verbose_name_plural': '设计数据备份',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IcpcBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True, verbose_name='版本')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='版本名称')),
                ('code', models.TextField(null=True, verbose_name='源代码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'ICPC数据备份',
                'verbose_name_plural': 'ICPC数据备份',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SourceCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True, verbose_name='版本')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='版本名称')),
                ('code', models.TextField(null=True, verbose_name='源代码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '作业系统脚本',
                'verbose_name_plural': '作业系统脚本',
                'ordering': ['id'],
            },
        ),
    ]
