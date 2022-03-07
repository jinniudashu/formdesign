# Generated by Django 4.0 on 2022-03-07 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0006_servicepackageevent_alter_serviceevent_service_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['id'], 'verbose_name': '单元服务', 'verbose_name_plural': '单元服务'},
        ),
        migrations.AlterModelOptions(
            name='serviceevent',
            options={'ordering': ['id'], 'verbose_name': '单元服务事件', 'verbose_name_plural': '单元服务事件'},
        ),
        migrations.AlterField(
            model_name='service',
            name='last_operation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_operation', to='define_operand.operation', verbose_name='结束作业'),
        ),
        migrations.AlterField(
            model_name='service',
            name='operations',
            field=models.ManyToManyField(blank=True, to='define_operand.Operation', verbose_name='可选作业'),
        ),
        migrations.AlterField(
            model_name='servicepackage',
            name='services',
            field=models.ManyToManyField(blank=True, to='define_operand.Service', verbose_name='可选服务'),
        ),
    ]
