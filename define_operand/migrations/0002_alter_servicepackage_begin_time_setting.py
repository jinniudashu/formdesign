# Generated by Django 4.0 on 2022-03-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepackage',
            name='begin_time_setting',
            field=models.PositiveSmallIntegerField(choices=[(0, '人工指定时间'), (1, '引用出生日期')], default=0, verbose_name='开始参考时间'),
        ),
    ]
