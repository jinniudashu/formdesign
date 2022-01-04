# Generated by Django 4.0 on 2021-12-30 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inquireform',
            options={'ordering': ['id'], 'verbose_name': '组合查询视图', 'verbose_name_plural': '组合查询视图'},
        ),
        migrations.AlterModelOptions(
            name='mutateform',
            options={'ordering': ['id'], 'verbose_name': '组合变更视图', 'verbose_name_plural': '组合变更视图'},
        ),
        migrations.AddField(
            model_name='inquireform',
            name='addforms',
            field=models.ManyToManyField(blank=True, to='define.InquireForm', verbose_name='查询视图'),
        ),
    ]
