# Generated by Django 4.0 on 2022-02-23 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0013_alter_service_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['id'], 'verbose_name': '规则', 'verbose_name_plural': '规则'},
        ),
    ]
