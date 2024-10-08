# Generated by Django 4.0 on 2023-09-11 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0005_alter_systemreservedfield_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemreservedfield',
            name='component',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='业务字段'),
        ),
        migrations.AlterField(
            model_name='systemreservedfield',
            name='type',
            field=models.CharField(choices=[('hssc_group_no', '组别'), ('hssc_charge_staff', '责任人'), ('hssc_operator', '作业人员'), ('hssc_scheduled_time', '计划执行时间'), ('hssc_duration', '时长'), ('hssc_frequency', '频次')], max_length=50, verbose_name='类型'),
        ),
    ]
