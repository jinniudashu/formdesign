# Generated by Django 4.0 on 2022-02-05 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0004_delete_operandview'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='版本')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='版本名称')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('code', models.TextField(verbose_name='源代码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '设计备份',
                'verbose_name_plural': '设计备份',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='sourcecode',
            options={'ordering': ['id'], 'verbose_name': '输出脚本', 'verbose_name_plural': '输出脚本'},
        ),
        migrations.AlterField(
            model_name='event',
            name='expression',
            field=models.TextField(blank=True, default='completed', help_text='\n        说明：<br>\n        1. 作业完成事件: completed<br>\n        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>\n        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"\n        ', max_length=1024, null=True, verbose_name='表达式'),
        ),
        migrations.AlterField(
            model_name='event_instructions',
            name='params',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='创建作业'),
        ),
    ]
