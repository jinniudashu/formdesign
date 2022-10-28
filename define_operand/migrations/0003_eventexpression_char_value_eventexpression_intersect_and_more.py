# Generated by Django 4.0 on 2022-10-28 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0002_remove_servicepackage_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventexpression',
            name='char_value',
            field=models.CharField(blank=True, help_text='多个值用英文逗号分隔，空格会被忽略', max_length=255, null=True, verbose_name='字符值'),
        ),
        migrations.AddField(
            model_name='eventexpression',
            name='intersect',
            field=models.BooleanField(default=False, verbose_name='交集'),
        ),
        migrations.AddField(
            model_name='eventexpression',
            name='number_value',
            field=models.FloatField(blank=True, null=True, verbose_name='数字值'),
        ),
        migrations.AlterField(
            model_name='eventexpression',
            name='value',
            field=models.CharField(max_length=255, null=True, verbose_name='值'),
        ),
    ]
