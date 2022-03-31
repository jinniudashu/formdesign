# Generated by Django 4.0 on 2022-03-29 15:51

import define_backup.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('define_icpc', '0001_initial'),
        ('define', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuessinessForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='表单说明')),
                ('meta_data', models.JSONField(blank=True, null=True, verbose_name='元数据')),
                ('script', models.TextField(blank=True, null=True, verbose_name='运行时脚本')),
                ('components', models.ManyToManyField(blank=True, to='define.Component', verbose_name='字段')),
                ('components_groups', models.ManyToManyField(blank=True, to='define.ComponentsGroup', verbose_name='组件')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '业务表单',
                'verbose_name_plural': '业务表单',
            },
            bases=(define_backup.mixins.GenerateModelsScriptMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BuessinessFormsSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('is_list', models.BooleanField(default=False, verbose_name='列表样式')),
                ('buessiness_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.buessinessform', verbose_name='表单')),
            ],
            options={
                'verbose_name': '作业表单设置',
                'verbose_name_plural': '作业表单设置',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name')),
                ('expression', models.TextField(blank=True, default='completed', help_text='\n        说明：<br>\n        1. 作业完成事件: completed<br>\n        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>\n        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"\n        ', max_length=1024, null=True, verbose_name='规则')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='事件描述')),
                ('parameters', models.CharField(blank=True, max_length=1024, null=True, verbose_name='检查字段')),
                ('fields', models.TextField(blank=True, max_length=1024, null=True, verbose_name='可用字段')),
                ('event_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='作业事件ID')),
            ],
            options={
                'verbose_name': '事件',
                'verbose_name_plural': '事件',
                'ordering': ['id'],
            },
        ),
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
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('code', models.CharField(max_length=10, verbose_name='指令代码')),
                ('func', models.CharField(max_length=100, verbose_name='操作函数')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='指令描述')),
            ],
            options={
                'verbose_name': '指令',
                'verbose_name_plural': '指令',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ManagedEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('app_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='所属app名')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='模型名')),
                ('base_form', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='define_operand.buessinessform', verbose_name='基础表单')),
            ],
            options={
                'verbose_name': '业务管理实体',
                'verbose_name_plural': '业务管理实体',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('execution_time_frame', models.DurationField(blank=True, null=True, verbose_name='执行时限')),
                ('awaiting_time_frame', models.DurationField(blank=True, null=True, verbose_name='等待执行时限')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('enable_queue_counter', models.BooleanField(default=True, verbose_name='显示队列数量')),
                ('suppliers', models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商')),
                ('not_suitable', models.CharField(blank=True, max_length=255, null=True, verbose_name='不适用对象')),
                ('time_limits', models.DurationField(blank=True, null=True, verbose_name='完成时限')),
                ('working_hours', models.DurationField(blank=True, null=True, verbose_name='工时')),
                ('frequency', models.CharField(blank=True, max_length=255, null=True, verbose_name='频次')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='成本')),
                ('load_feedback', models.BooleanField(default=False, verbose_name='是否反馈负荷数量')),
                ('resource_materials', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套物料')),
                ('resource_devices', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套设备')),
                ('resource_knowledge', models.CharField(blank=True, max_length=255, null=True, verbose_name='服务知识')),
                ('buessiness_forms', models.ManyToManyField(through='define_operand.BuessinessFormsSetting', to='define_operand.BuessinessForm', verbose_name='作业表单')),
                ('group', models.ManyToManyField(blank=True, to='define.Role', verbose_name='作业角色')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '作业',
                'verbose_name_plural': '作业',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=255, verbose_name='名称')),
                ('begin_time_setting', models.PositiveSmallIntegerField(choices=[(0, '人工指定时间'), (1, '引用出生日期')], default=0, verbose_name='开始时间设置')),
                ('execution_time_frame', models.DurationField(blank=True, null=True, verbose_name='执行时限')),
                ('awaiting_time_frame', models.DurationField(blank=True, null=True, verbose_name='等待执行时限')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('history_services_display', models.PositiveBigIntegerField(blank=True, choices=[(0, '所有历史服务'), (1, '当日服务')], default=0, null=True, verbose_name='历史服务默认显示')),
                ('enable_recommanded_list', models.BooleanField(default=True, verbose_name='显示推荐作业')),
                ('enable_queue_counter', models.BooleanField(default=True, verbose_name='显示队列计数')),
                ('suppliers', models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商')),
                ('not_suitable', models.CharField(blank=True, max_length=255, null=True, verbose_name='不适用对象')),
                ('time_limits', models.DurationField(blank=True, null=True, verbose_name='完成时限')),
                ('working_hours', models.DurationField(blank=True, null=True, verbose_name='工时')),
                ('frequency', models.CharField(blank=True, max_length=255, null=True, verbose_name='频次')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='成本')),
                ('load_feedback', models.BooleanField(default=False, verbose_name='是否反馈负荷数量')),
                ('resource_materials', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套物料')),
                ('resource_devices', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套设备')),
                ('resource_knowledge', models.CharField(blank=True, max_length=255, null=True, verbose_name='服务知识')),
                ('script', models.TextField(blank=True, help_text="script['views'] , script['urls'], script['templates']", null=True, verbose_name='运行时脚本')),
                ('group', models.ManyToManyField(to='define.Role', verbose_name='服务角色')),
                ('managed_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.managedentity', verbose_name='管理实体')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '服务',
                'verbose_name_plural': '服务',
                'ordering': ['id'],
            },
            bases=(define_backup.mixins.GenerateViewsScriptMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('begin_time_setting', models.PositiveSmallIntegerField(choices=[(0, '人工指定'), (1, '出生日期')], default=0, verbose_name='开始时间参考')),
                ('duration', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='持续周期')),
                ('execution_time_frame', models.DurationField(blank=True, null=True, verbose_name='执行时限')),
                ('awaiting_time_frame', models.DurationField(blank=True, null=True, verbose_name='等待执行时限')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '服务包',
                'verbose_name_plural': '服务包',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
            ],
            options={
                'verbose_name': '服务规则',
                'verbose_name_plural': '服务规则',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SystemOperand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('func', models.CharField(blank=True, max_length=255, null=True, verbose_name='内部实现函数')),
                ('parameters', models.CharField(blank=True, max_length=255, null=True, verbose_name='参数')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('applicable', models.PositiveSmallIntegerField(choices=[(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')], default=1, verbose_name='适用范围')),
            ],
            options={
                'verbose_name': '系统自动作业',
                'verbose_name_plural': '系统自动作业',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceProgramSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('passing_data', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')], default=0, null=True, verbose_name='接收表单')),
                ('complete_feedback', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '返回完成状态'), (2, '返回表单')], default=0, null=True, verbose_name='完成反馈')),
                ('reminders', models.PositiveSmallIntegerField(blank=True, choices=[(0, '客户'), (1, '服务人员'), (2, '服务小组')], default=0, null=True, verbose_name='提醒对象')),
                ('message_content', models.CharField(blank=True, max_length=255, null=True, verbose_name='消息内容')),
                ('interval_rule', models.PositiveSmallIntegerField(blank=True, choices=[(0, '等于'), (1, '小于'), (2, '大于')], null=True, verbose_name='间隔条件')),
                ('interval_time', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='间隔时间')),
                ('is_active', models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')),
                ('event_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.eventrule', verbose_name='条件事件')),
                ('next_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_service', to='define_operand.service', verbose_name='后续服务')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='服务项目')),
                ('service_spec', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.servicespec', verbose_name='服务规格')),
                ('system_operand', models.ForeignKey(blank=True, limit_choices_to=models.Q(('applicable__in', [1, 3])), null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.systemoperand', verbose_name='系统作业')),
            ],
            options={
                'verbose_name': '服务程序设置',
                'verbose_name_plural': '服务程序设置',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServicePackageDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('cycle_option', models.PositiveSmallIntegerField(blank=True, choices=[(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')], default=0, null=True, verbose_name='周期')),
                ('cycle_times', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='次数')),
                ('reference_start_tim', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='参考起始时间')),
                ('duration', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='持续周期')),
                ('check_awaiting_timeout', models.BooleanField(default=False, verbose_name='检查等待超时')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='服务项目')),
                ('servicepackage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.servicepackage', verbose_name='服务包')),
            ],
            options={
                'verbose_name': '服务内容模板',
                'verbose_name_plural': '服务内容模板',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='servicepackage',
            name='services',
            field=models.ManyToManyField(through='define_operand.ServicePackageDetail', to='define_operand.Service', verbose_name='服务项目'),
        ),
        migrations.CreateModel(
            name='OperationsSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('passing_data', models.PositiveSmallIntegerField(choices=[(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')], default=0, verbose_name='接收表单')),
                ('event_rule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.eventrule', verbose_name='条件事件')),
                ('next_operation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_operation', to='define_operand.operation', verbose_name='后续作业')),
                ('operation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.operation', verbose_name='作业')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='单元服务')),
                ('system_operand', models.ForeignKey(blank=True, limit_choices_to=models.Q(('applicable__in', [0, 3])), null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.systemoperand', verbose_name='系统作业')),
            ],
            options={
                'verbose_name': '作业关系设置',
                'verbose_name_plural': '作业关系设置',
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
                ('operator', models.PositiveSmallIntegerField(choices=[(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<='), (6, 'in'), (7, 'not in')], null=True, verbose_name='操作符')),
                ('value', models.CharField(help_text='多个值用英文逗号分隔，空格会被忽略', max_length=255, null=True, verbose_name='值')),
                ('connection_operator', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'and'), (1, 'or')], null=True, verbose_name='连接操作符')),
                ('event_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.eventrule', verbose_name='事件规则')),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='字段')),
            ],
            options={
                'verbose_name': '事件表达式',
                'verbose_name_plural': '事件表达式',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Event_instructions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=1, verbose_name='指令序号')),
                ('params', models.CharField(blank=True, max_length=255, null=True, verbose_name='创建作业')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.event', verbose_name='事件')),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.instruction', verbose_name='指令')),
            ],
            options={
                'verbose_name': '作业事件指令集',
                'verbose_name_plural': '作业事件指令集',
                'ordering': ['event', 'order'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='next_operations',
            field=models.ManyToManyField(to='define_operand.Operation', verbose_name='后续作业'),
        ),
        migrations.AddField(
            model_name='event',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_oid', to='define_operand.operation', verbose_name='所属作业'),
        ),
        migrations.AddField(
            model_name='buessinessformssetting',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.operation', verbose_name='作业'),
        ),
    ]
