# Generated by Django 4.0 on 2021-12-10 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0003_boolfield_alter_baseform_name_alter_basemodel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boolfield',
            name='default',
            field=models.CharField(blank=True, choices=[('0', '否'), ('1', '是'), ('2', '未知')], max_length=10, null=True, verbose_name='默认值'),
        ),
    ]
