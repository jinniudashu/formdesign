# Generated by Django 4.0 on 2022-06-09 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0005_alter_relatedfield_related_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characterfield',
            name='label',
            field=models.CharField(max_length=63, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='characterfield',
            name='name',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='dtfield',
            name='label',
            field=models.CharField(max_length=63, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='dtfield',
            name='name',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='filefield',
            name='label',
            field=models.CharField(max_length=63, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='filefield',
            name='name',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='numberfield',
            name='label',
            field=models.CharField(max_length=63, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='numberfield',
            name='name',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='relatedfield',
            name='label',
            field=models.CharField(max_length=63, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='relatedfield',
            name='name',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='name'),
        ),
    ]
