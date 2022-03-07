# Generated by Django 4.0 on 2022-03-07 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0007_alter_service_options_alter_serviceevent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='指令名称'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='role',
            name='label',
            field=models.CharField(max_length=255, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='label',
            field=models.CharField(max_length=255, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='serviceevent',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='serviceevent',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='servicepackage',
            name='label',
            field=models.CharField(max_length=255, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='servicepackage',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='servicepackageevent',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='servicepackageevent',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name'),
        ),
    ]
