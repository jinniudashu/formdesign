# Generated by Django 4.0 on 2022-03-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0002_remove_buessinessform_buessiness_form_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='instruction_id',
        ),
        migrations.RemoveField(
            model_name='role',
            name='role_id',
        ),
        migrations.RemoveField(
            model_name='systemoperand',
            name='system_action_id',
        ),
        migrations.AddField(
            model_name='instruction',
            name='hssc_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID'),
        ),
        migrations.AddField(
            model_name='role',
            name='hssc_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID'),
        ),
        migrations.AddField(
            model_name='systemoperand',
            name='hssc_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='role',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='systemoperand',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
    ]
