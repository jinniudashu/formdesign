# Generated by Django 4.0 on 2022-02-24 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_dict', '0003_dicdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dicdetail',
            name='diclist',
        ),
        migrations.RemoveField(
            model_name='dicdetail',
            name='icpc',
        ),
    ]
