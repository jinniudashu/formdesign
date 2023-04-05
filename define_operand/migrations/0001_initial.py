# Generated by Django 4.0 on 2023-04-05 10:05

import define_operand.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('define', '0001_initial'),
        ('define_icpc', '0001_initial'),
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
                ('api_fields', models.JSONField(blank=True, null=True, verbose_name='API字段')),
            ],
            options={
                'verbose_name': '业务表单',
                'verbose_name_plural': '业务表单',
            },
            bases=(define_operand.models.GenerateFormsScriptMixin, models.Model),
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
                'verbose_name': '服务表单设置',
                'verbose_name_plural': '服务表单设置',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CoreModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='模型名')),
            ],
            options={
                'verbose_name': '内核模型',
                'verbose_name_plural': '内核模型',
            },
        ),
        migrations.CreateModel(
            name='CycleUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('cycle_unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='周期单位')),
                ('days', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='天数')),
            ],
            options={
                'verbose_name': '服务周期单位',
                'verbose_name_plural': '服务周期单位',
            },
        ),
        migrations.CreateModel(
            name='EventRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='表达式')),
                ('detection_scope', models.CharField(blank=True, choices=[('ALL', '所有历史表单'), ('CURRENT_SERVICE', '本次服务表单'), ('LAST_WEEK_SERVICES', '过去7天表单')], default='CURRENT_SERVICE', max_length=100, null=True, verbose_name='检测范围')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='权重')),
                ('expression', models.TextField(blank=True, max_length=1024, null=True, verbose_name='内部表达式')),
                ('expression_fields', models.CharField(blank=True, max_length=1024, null=True, verbose_name='内部表达式字段')),
            ],
            options={
                'verbose_name': '条件事件',
                'verbose_name_plural': '条件事件',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ExternalServiceMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('external_form_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='外部表单标识')),
                ('external_form_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='外部表单名称')),
                ('form_source', models.CharField(blank=True, choices=[('jinshuju', '金数据'), ('other', '其它')], max_length=50, null=True, verbose_name='来源名称')),
                ('fields_mapping', models.JSONField(blank=True, null=True, verbose_name='字段映射')),
            ],
            options={
                'verbose_name': '外部服务映射',
                'verbose_name_plural': '外部服务映射',
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
                ('header_fields_json', models.JSONField(blank=True, null=True, verbose_name='表头字段json')),
                ('base_form', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='define_operand.buessinessform', verbose_name='基础表单')),
                ('header_fields', models.ManyToManyField(blank=True, to='define.Component', verbose_name='表头字段')),
            ],
            options={
                'verbose_name': '管理实体',
                'verbose_name_plural': '管理实体',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('service_type', models.PositiveSmallIntegerField(choices=[(0, '系统服务'), (1, '管理调度服务'), (2, '诊疗服务')], default=2, verbose_name='服务类型')),
                ('history_services_display', models.PositiveBigIntegerField(blank=True, choices=[(0, '所有历史服务'), (1, '当日服务')], default=0, null=True, verbose_name='历史服务默认显示')),
                ('enable_queue_counter', models.BooleanField(default=True, verbose_name='显示队列数量')),
                ('route_to', models.CharField(blank=True, choices=[('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')], default='CUSTOMER_HOMEPAGE', max_length=50, null=True, verbose_name='完成跳转至')),
                ('follow_up_required', models.BooleanField(default=False, verbose_name='需要随访')),
                ('follow_up_interval', models.DurationField(blank=True, null=True, verbose_name='随访间隔')),
                ('suppliers', models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商')),
                ('not_suitable', models.CharField(blank=True, max_length=255, null=True, verbose_name='不适用对象')),
                ('overtime', models.DurationField(blank=True, null=True, verbose_name='超期时限')),
                ('working_hours', models.DurationField(blank=True, null=True, verbose_name='工时')),
                ('frequency', models.CharField(blank=True, max_length=255, null=True, verbose_name='频次')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='成本')),
                ('load_feedback', models.BooleanField(default=False, verbose_name='是否反馈负荷数量')),
                ('resource_materials', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套物料')),
                ('resource_devices', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套设备')),
                ('resource_knowledge', models.CharField(blank=True, max_length=255, null=True, verbose_name='服务知识')),
                ('generate_script_order', models.PositiveSmallIntegerField(default=100, verbose_name='生成脚本顺序')),
                ('buessiness_forms', models.ManyToManyField(through='define_operand.BuessinessFormsSetting', to='define_operand.BuessinessForm', verbose_name='作业表单')),
                ('follow_up_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follow_up_services', to='define_operand.service', verbose_name='随访服务')),
                ('managed_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.managedentity', verbose_name='管理实体')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
                ('role', models.ManyToManyField(blank=True, to='define.Role', verbose_name='服务岗位')),
            ],
            options={
                'verbose_name': '服务',
                'verbose_name_plural': '服务',
                'ordering': ['id'],
            },
            bases=(define_operand.models.GenerateServiceScriptMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '服务包',
                'verbose_name_plural': '服务包',
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
            ],
            options={
                'verbose_name': '系统自动作业',
                'verbose_name_plural': '系统自动作业',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('passing_data', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')], default=0, null=True, verbose_name='接收表单')),
                ('complete_feedback', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '返回完成状态'), (2, '返回表单')], default=0, null=True, verbose_name='完成反馈')),
                ('reminders', models.PositiveSmallIntegerField(blank=True, choices=[(0, '客户'), (1, '服务人员'), (2, '服务小组')], default=0, null=True, verbose_name='提醒对象')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='消息内容')),
                ('interval_rule', models.PositiveSmallIntegerField(blank=True, choices=[(0, '等于'), (1, '小于'), (2, '大于')], null=True, verbose_name='间隔条件')),
                ('interval_time', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='间隔时间')),
                ('is_active', models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')),
                ('event_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.eventrule', verbose_name='条件事件')),
                ('next_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_service', to='define_operand.service', verbose_name='后续服务')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='服务项目')),
                ('system_operand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.systemoperand', verbose_name='系统作业')),
            ],
            options={
                'verbose_name': '服务规则',
                'verbose_name_plural': '服务规则',
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
                ('order', models.PositiveSmallIntegerField(default=100, verbose_name='顺序')),
                ('cycle_frequency', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='每周期频次')),
                ('cycle_times', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='天数')),
                ('default_beginning_time', models.PositiveSmallIntegerField(choices=[(1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')], default=1, verbose_name='执行时间基准')),
                ('base_interval', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='基准间隔')),
                ('cycle_unit', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.cycleunit', verbose_name='周期单位')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='服务项目')),
                ('servicepackage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.servicepackage', verbose_name='服务包')),
            ],
            options={
                'verbose_name': '服务内容模板',
                'verbose_name_plural': '服务内容模板',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目描述')),
                ('external_services', models.ManyToManyField(blank=True, to='define_operand.ExternalServiceMapping', verbose_name='外部服务映射')),
                ('roles', models.ManyToManyField(blank=True, to='define.Role', verbose_name='角色')),
                ('service_packages', models.ManyToManyField(blank=True, to='define_operand.ServicePackage', verbose_name='服务包')),
                ('service_rules', models.ManyToManyField(blank=True, to='define_operand.ServiceRule', verbose_name='服务规则')),
                ('services', models.ManyToManyField(blank=True, to='define_operand.Service', verbose_name='服务')),
            ],
            options={
                'verbose_name': '项目列表',
                'verbose_name_plural': '项目列表',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='managedentity',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='define_operand.project', verbose_name='所属项目'),
        ),
        migrations.CreateModel(
            name='FormComponentsSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('is_required', models.BooleanField(default=False, verbose_name='是否必填')),
                ('api_field', models.CharField(blank=True, choices=[('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间')], max_length=50, null=True, verbose_name='对接系统接口')),
                ('position', models.PositiveSmallIntegerField(default=100, verbose_name='位置顺序')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='字段')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.buessinessform', verbose_name='表单')),
            ],
            options={
                'verbose_name': '表单组件设置',
                'verbose_name_plural': '表单组件设置',
            },
        ),
        migrations.AddField(
            model_name='externalservicemapping',
            name='service',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='对应服务'),
        ),
        migrations.CreateModel(
            name='ExternalServiceFieldsMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('external_field_name', models.CharField(max_length=100, null=True, verbose_name='外部字段名称')),
                ('external_form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define_operand.externalservicemapping', verbose_name='外部表单')),
                ('service_form_field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='服务表单字段')),
            ],
            options={
                'verbose_name': '外部服务字段映射',
                'verbose_name_plural': '外部服务字段映射',
            },
        ),
        migrations.CreateModel(
            name='EventExpression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('char_value', models.CharField(blank=True, help_text='多个值用英文逗号分隔，空格会被忽略', max_length=255, null=True, verbose_name='字符值')),
                ('operator', models.PositiveSmallIntegerField(choices=[(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<=')], null=True, verbose_name='操作符')),
                ('number_value', models.FloatField(blank=True, null=True, verbose_name='数字值')),
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
        migrations.AddField(
            model_name='buessinessformssetting',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='define_operand.service', verbose_name='作业'),
        ),
        migrations.AddField(
            model_name='buessinessform',
            name='components',
            field=models.ManyToManyField(through='define_operand.FormComponentsSetting', to='define.Component', verbose_name='字段'),
        ),
        migrations.AddField(
            model_name='buessinessform',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
    ]
