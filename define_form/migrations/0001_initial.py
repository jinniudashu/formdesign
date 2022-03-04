# Generated by Django 4.0 on 2022-03-04 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('define_dict', '0001_initial'),
        ('define', '0001_initial'),
        ('define_icpc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='视图名称')),
                ('is_inquiry', models.BooleanField(default=False, verbose_name='仅用于查询')),
                ('style', models.CharField(choices=[('detail', '详情'), ('list', '列表')], default='detail', max_length=50, verbose_name='风格')),
                ('meta_data', models.JSONField(blank=True, null=True, verbose_name='视图元数据')),
                ('baseform_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='基础视图ID')),
            ],
            options={
                'verbose_name': '基础视图',
                'verbose_name_plural': '基础视图',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CombineForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='表单名称')),
                ('is_base', models.BooleanField(default=False, verbose_name='基础视图')),
                ('meta_data', models.JSONField(blank=True, null=True, verbose_name='视图元数据')),
                ('combineform_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='组合视图ID')),
                ('forms', models.ManyToManyField(blank=True, to='define_form.BaseForm', verbose_name='可用视图')),
                ('managed_entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_dict.managedentity', verbose_name='实体类型')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '组合视图',
                'verbose_name_plural': '组合视图',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='表单名称')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('is_base_infomation', models.BooleanField(default=False, verbose_name='基础信息表')),
                ('basemodel_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='基础表单ID')),
                ('components', models.ManyToManyField(to='define.Component', verbose_name='字段')),
                ('managed_entity', models.ManyToManyField(blank=True, to='define_dict.ManagedEntity', verbose_name='关联实体')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '基础表单',
                'verbose_name_plural': '基础表单',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='baseform',
            name='basemodel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_form.basemodel', verbose_name='基础表单'),
        ),
        migrations.AddField(
            model_name='baseform',
            name='components',
            field=models.ManyToManyField(to='define.Component', verbose_name='字段'),
        ),
    ]
