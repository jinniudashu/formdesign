# Generated by Django 4.0 on 2022-03-15 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0002_servicessetting_check_awaiting_timeout_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicessetting',
            name='accepting_confirm',
        ),
    ]
