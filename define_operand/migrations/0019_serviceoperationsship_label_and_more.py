# Generated by Django 4.0 on 2022-03-10 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0018_alter_frequencyrule_cycle_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceoperationsship',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='serviceoperationsship',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='servicepackageservicesship',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='servicepackageservicesship',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
    ]
