# Generated by Django 4.0 on 2022-03-09 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0008_serviceoperationsship_remove_service_operations_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SystemAction',
            new_name='SystemOperand',
        ),
        migrations.RenameField(
            model_name='serviceoperationsship',
            old_name='system_action',
            new_name='system_operand',
        ),
    ]
