# Generated by Django 4.0 on 2022-03-03 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('define_icpc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputeField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RelateFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='关联模型名称')),
                ('related_content', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联内容')),
                ('display_field', models.CharField(blank=True, max_length=100, null=True, verbose_name='显示字段')),
                ('related_field', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联字段')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('relate_field_model_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='关联字段基础表ID')),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'define_dict'), models.Q(('model', 'diclist'), ('model', 'managedentity'), _connector='OR')), ('app_label', 'define_icpc'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='关联基本信息')),
            ],
            options={
                'verbose_name': '关联字段基础表',
                'verbose_name_plural': '关联字段基础表',
            },
        ),
        migrations.CreateModel(
            name='RelatedField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')], default='ChoiceField', max_length=50, verbose_name='类型')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
                ('related_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define.relatefieldmodel', verbose_name='关联内容')),
            ],
            options={
                'verbose_name': '关联字段',
                'verbose_name_plural': '关联字段',
            },
        ),
        migrations.CreateModel(
            name='NumberField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')], default='IntegerField', max_length=50, verbose_name='类型')),
                ('max_digits', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='最大位数')),
                ('decimal_places', models.PositiveSmallIntegerField(blank=True, default=2, null=True, verbose_name='小数位数')),
                ('standard_value', models.FloatField(blank=True, null=True, verbose_name='标准值')),
                ('up_limit', models.FloatField(blank=True, null=True, verbose_name='上限')),
                ('down_limit', models.FloatField(blank=True, null=True, verbose_name='下限')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='单位')),
                ('default', models.FloatField(blank=True, null=True, verbose_name='默认值')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '数值字段',
                'verbose_name_plural': '数值字段',
            },
        ),
        migrations.CreateModel(
            name='DTField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('DateTimeField', '日期时间'), ('DateField', '日期')], default='DateTimeField', max_length=50, verbose_name='类型')),
                ('default_now', models.BooleanField(default=False, verbose_name='默认为当前时间')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '日期字段',
                'verbose_name_plural': '日期字段',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(blank=True, max_length=100, null=True, verbose_name='表单字段')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(('app_label', 'define'), models.Q(('model', 'boolfield'), ('model', 'characterfield'), ('model', 'numberfield'), ('model', 'dtfield'), ('model', 'choicefield'), ('model', 'relatedfield'), ('model', 'computefield'), _connector='OR')), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': '表单字段汇总',
                'verbose_name_plural': '表单字段汇总',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ChoiceField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')], default='ChoiceField', max_length=50, verbose_name='类型')),
                ('options', models.TextField(blank=True, help_text='每行一个选项, 最多100个', max_length=1024, null=True, verbose_name='选项')),
                ('default_first', models.BooleanField(default=False, verbose_name='默认选第一个')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '选择字段',
                'verbose_name_plural': '选择字段',
            },
        ),
        migrations.CreateModel(
            name='CharacterField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('CharField', '单行文本'), ('TextField', '多行文本')], default='CharField', max_length=50, verbose_name='类型')),
                ('length', models.PositiveSmallIntegerField(default=255, verbose_name='字符长度')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('default', models.CharField(blank=True, max_length=255, null=True, verbose_name='默认值')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '字符字段',
                'verbose_name_plural': '字符字段',
            },
        ),
        migrations.CreateModel(
            name='BoolField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='name')),
                ('label', models.CharField(max_length=100, verbose_name='表单字段')),
                ('type', models.CharField(choices=[('0', '是, 否'), ('1', '未知, 是, 否')], default='1', max_length=100, verbose_name='可选值')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('default', models.CharField(blank=True, choices=[('0', '未知'), ('1', '是'), ('2', '否')], default='0', max_length=10, null=True, verbose_name='默认值')),
                ('field_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='字段ID')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '是否字段',
                'verbose_name_plural': '是否字段',
            },
        ),
    ]
