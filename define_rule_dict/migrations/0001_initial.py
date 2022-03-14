# Generated by Django 4.0 on 2022-03-14 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('define', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='表达式')),
                ('detection_scope', models.PositiveSmallIntegerField(blank=True, choices=[(0, '所有历史表单'), (1, '本次服务表单'), (2, '单元服务表单')], default=1, null=True, verbose_name='检测范围')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='权重')),
                ('expression', models.TextField(blank=True, max_length=1024, null=True, verbose_name='内部表达式')),
            ],
            options={
                'verbose_name': '条件事件',
                'verbose_name_plural': '条件事件',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FrequencyRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('cycle_option', models.PositiveSmallIntegerField(blank=True, choices=[(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')], default=0, null=True, verbose_name='周期')),
                ('times', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='次数')),
            ],
            options={
                'verbose_name': '频度规则',
                'verbose_name_plural': '频度规则',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IntervalRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('rule', models.PositiveSmallIntegerField(blank=True, choices=[(0, '等于'), (1, '小于'), (2, '大于')], null=True, verbose_name='间隔规则')),
                ('interval', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='间隔时间')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='说明')),
            ],
            options={
                'verbose_name': '间隔规则',
                'verbose_name_plural': '间隔规则',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='EventExpression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('operator', models.PositiveSmallIntegerField(blank=True, choices=[(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<='), (6, 'in'), (7, 'not in')], null=True, verbose_name='操作符')),
                ('value', models.CharField(blank=True, help_text='多个值用英文逗号分隔，空格会被忽略', max_length=255, null=True, verbose_name='值')),
                ('connection_operator', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'and'), (1, 'or')], null=True, verbose_name='连接操作符')),
                ('event_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_rule_dict.eventrule', verbose_name='事件规则')),
                ('field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='字段')),
            ],
            options={
                'verbose_name': '事件表达式',
                'verbose_name_plural': '事件表达式',
                'ordering': ['id'],
            },
        ),
    ]
