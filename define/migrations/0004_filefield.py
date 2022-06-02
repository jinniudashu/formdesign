# Generated by Django 4.0 on 2022-06-02 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('define_icpc', '0001_initial'),
        ('define', '0003_rename_medcine_medicine_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('type', models.CharField(choices=[('ImageField', '图片'), ('FileField', '文件')], default='ImageField', max_length=50, verbose_name='类型')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '文件字段',
                'verbose_name_plural': '文件字段',
            },
        ),
    ]
