# Generated by Django 4.0 on 2023-04-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0002_computecomponentssetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computecomponentssetting',
            name='description',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='计算逻辑说明'),
        ),
        migrations.AlterField(
            model_name='computecomponentssetting',
            name='js_script',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name='计算脚本'),
        ),
    ]
