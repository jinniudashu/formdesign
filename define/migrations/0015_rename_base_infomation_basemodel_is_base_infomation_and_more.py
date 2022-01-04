# Generated by Django 4.0 on 2022-01-02 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0014_baseform_meta_data_combineform_meta_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basemodel',
            old_name='base_infomation',
            new_name='is_base_infomation',
        ),
        migrations.RemoveField(
            model_name='baseform',
            name='fields',
        ),
        migrations.RemoveField(
            model_name='combineform',
            name='inquiry_fields',
        ),
        migrations.RemoveField(
            model_name='combineform',
            name='mutate_fields',
        ),
        migrations.AlterField(
            model_name='baseform',
            name='meta_data',
            field=models.JSONField(blank=True, null=True, verbose_name='视图元数据'),
        ),
    ]
