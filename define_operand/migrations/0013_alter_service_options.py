# Generated by Django 4.0 on 2022-02-23 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0012_alter_operation_name_new'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['id'], 'verbose_name': '单元服务', 'verbose_name_plural': '单元服务'},
        ),
    ]
