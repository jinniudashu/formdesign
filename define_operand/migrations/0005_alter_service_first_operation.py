# Generated by Django 4.0 on 2022-02-08 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0004_alter_operation_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='first_operation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_operation', to='define_operand.operation', verbose_name='起始作业'),
        ),
    ]
