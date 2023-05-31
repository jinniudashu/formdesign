# Generated by Django 4.0 on 2023-05-31 07:34

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
            name='DicList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '自定义关联字典',
                'verbose_name_plural': '自定义关联字典',
            },
        ),
        migrations.CreateModel(
            name='IcpcList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('app_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='所属app名')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='模型名')),
            ],
            options={
                'verbose_name': 'ICPC字典列表',
                'verbose_name_plural': 'ICPC字典列表',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('yp_code', models.CharField(max_length=10, null=True, verbose_name='药品编码')),
                ('specification', models.CharField(max_length=100, null=True, verbose_name='规格')),
                ('measure', models.CharField(max_length=30, null=True, verbose_name='单位')),
                ('mz_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='门诊参考单价')),
                ('usage', models.CharField(max_length=60, null=True, verbose_name='用法')),
                ('dosage', models.CharField(max_length=60, null=True, verbose_name='用量')),
                ('type', models.CharField(max_length=40, null=True, verbose_name='药剂类型')),
                ('yp_sort', models.CharField(max_length=60, null=True, verbose_name='药品分类名称')),
                ('current_storage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='当前库存')),
                ('cf_measure', models.CharField(max_length=30, null=True, verbose_name='处方计量单位')),
                ('xs_measure', models.CharField(max_length=30, null=True, verbose_name='销售计量单位')),
                ('cf_dosage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='常用单次处方用量(处方单位)')),
                ('not_cfyp', models.BooleanField(default=False, verbose_name='非处方药标记')),
                ('mzcf_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='门诊处方价格')),
                ('is_use', models.BooleanField(default=True, verbose_name='是否使用中')),
                ('ypty_name', models.CharField(max_length=200, null=True, verbose_name='药品通用名称')),
                ('gjjbyp', models.CharField(max_length=100, null=True, verbose_name='国家基本药品目录名称')),
                ('ybypbm', models.CharField(max_length=100, null=True, verbose_name='医保药品目录对应药品编码')),
                ('ybyplb', models.CharField(max_length=2, null=True, verbose_name='药品报销类别（甲类、乙类）')),
                ('syz', models.CharField(max_length=255, null=True, verbose_name='适应症')),
                ('bsyz', models.CharField(max_length=255, null=True, verbose_name='不适应症')),
                ('fytj', models.CharField(max_length=255, null=True, verbose_name='服用途径')),
                ('fypc', models.CharField(max_length=255, null=True, verbose_name='服用频次')),
                ('fyzysxhbz', models.CharField(max_length=255, null=True, verbose_name='服用注意事项和备注')),
            ],
            options={
                'verbose_name': '药品基本信息表',
                'verbose_name_plural': '药品基本信息表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='MedicineImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('YPCode', models.CharField(max_length=10, verbose_name='药品编码')),
                ('PYM', models.CharField(max_length=100, null=True, verbose_name='拼音码')),
                ('YPName', models.CharField(max_length=200, null=True, verbose_name='药品名称')),
                ('Specification', models.CharField(max_length=100, null=True, verbose_name='规格')),
                ('Measure', models.CharField(max_length=30, null=True, verbose_name='单位')),
                ('MZPrice', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='门诊参考单价')),
                ('Usage', models.CharField(max_length=60, null=True, verbose_name='用法')),
                ('Dosage', models.CharField(max_length=60, null=True, verbose_name='用量')),
                ('Type', models.CharField(max_length=40, null=True, verbose_name='药剂类型')),
                ('YPSort', models.CharField(max_length=60, null=True, verbose_name='药品分类名称')),
                ('MaxStorage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='最大库存')),
                ('MinStorage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='最小库存')),
                ('CurrentStorage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='当前库存')),
                ('CFMeasure', models.CharField(max_length=30, null=True, verbose_name='处方计量单位')),
                ('XSMeasure', models.CharField(max_length=30, null=True, verbose_name='销售计量单位')),
                ('RK2XS', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='计量单位换算（入库销售）')),
                ('XS2CF', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='计量单位换算（销售处方）')),
                ('AllowBreak', models.BooleanField(default=False, verbose_name='允许拆散销售')),
                ('PricePercentLS', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='拆散零售价制定比例')),
                ('PricePercentXS', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='正常销售价制定比例')),
                ('EconomyBatch', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='经济批量')),
                ('MinBuy', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='最小订货量')),
                ('CountForCode', models.CharField(max_length=10, null=True, verbose_name='价值分类码')),
                ('CFDosage', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='常用单次处方用量(处方单位)')),
                ('NotCFYP', models.BooleanField(default=False, verbose_name='非处方药标记')),
                ('IsSurveillant', models.BooleanField(default=False, verbose_name='是否为监测使用')),
                ('Cycle', models.BooleanField(default=False, verbose_name='循环盘点标志')),
                ('LastCycleDate', models.DateTimeField(null=True, verbose_name='上次盘点时间')),
                ('Anaphylaxis', models.BooleanField(default=False, verbose_name='药品过敏标识')),
                ('isXY', models.BooleanField(default=False, verbose_name='为西药')),
                ('isAppliance', models.BooleanField(default=False, verbose_name='为医用器材(耗材)')),
                ('isCHN', models.BooleanField(default=False, verbose_name='为中药药材')),
                ('isNew', models.BooleanField(default=False, verbose_name='新药标识')),
                ('WJH', models.CharField(max_length=50, null=True, verbose_name='存放货架号')),
                ('CFCM', models.CharField(max_length=30, null=True, verbose_name='存放的层位码')),
                ('MZPriceCF', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='门诊处方价格')),
                ('IsUse', models.BooleanField(default=True, verbose_name='是否使用中')),
                ('YptyName', models.CharField(max_length=200, null=True, verbose_name='药品通用名称')),
                ('gjjbyp', models.CharField(max_length=100, null=True, verbose_name='国家基本药品目录名称')),
                ('ybypbm', models.CharField(max_length=100, null=True, verbose_name='医保药品目录对应药品编码')),
                ('ybyplb', models.CharField(max_length=2, null=True, verbose_name='药品报销类别（甲类、乙类）')),
                ('syz', models.CharField(max_length=255, null=True, verbose_name='适应症')),
                ('bsyz', models.CharField(max_length=255, null=True, verbose_name='不适应症')),
                ('fytj', models.CharField(max_length=255, null=True, verbose_name='服用途径')),
                ('fypc', models.CharField(max_length=255, null=True, verbose_name='服用频次')),
                ('fyzysxhbz', models.CharField(max_length=255, null=True, verbose_name='服用注意事项和备注')),
            ],
            options={
                'verbose_name': '药品基本信息导入表',
                'verbose_name_plural': '药品基本信息导入表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RelateFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('related_content', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联内容')),
                ('related_content_type', models.CharField(choices=[('dictionaries', '基础字典'), ('icpc', 'ICPC'), ('service', '管理实体'), ('core', '内核')], default=0, max_length=20, verbose_name='关联内容类型')),
            ],
            options={
                'verbose_name': '关联字段基础表',
                'verbose_name_plural': '关联字段基础表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位描述')),
            ],
            options={
                'verbose_name': '业务岗位',
                'verbose_name_plural': '业务岗位',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RelatedField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('label', models.CharField(max_length=63, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=63, null=True, verbose_name='name')),
                ('type', models.CharField(choices=[('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')], default='ChoiceField', max_length=50, verbose_name='类型')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
                ('related_content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='define.relatefieldmodel', verbose_name='关联内容')),
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
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('label', models.CharField(max_length=63, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=63, null=True, verbose_name='name')),
                ('type', models.CharField(choices=[('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')], default='IntegerField', max_length=50, verbose_name='类型')),
                ('max_digits', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='最大位数')),
                ('decimal_places', models.PositiveSmallIntegerField(blank=True, default=2, null=True, verbose_name='小数位数')),
                ('standard_value', models.FloatField(blank=True, null=True, verbose_name='标准值')),
                ('up_limit', models.FloatField(blank=True, null=True, verbose_name='上限')),
                ('down_limit', models.FloatField(blank=True, null=True, verbose_name='下限')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='单位')),
                ('default', models.FloatField(blank=True, null=True, verbose_name='默认值')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '数值字段',
                'verbose_name_plural': '数值字段',
            },
        ),
        migrations.CreateModel(
            name='FileField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('label', models.CharField(max_length=63, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=63, null=True, verbose_name='name')),
                ('type', models.CharField(choices=[('ImageField', '图片'), ('FileField', '文件')], default='ImageField', max_length=50, verbose_name='类型')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '文件字段',
                'verbose_name_plural': '文件字段',
            },
        ),
        migrations.CreateModel(
            name='DTField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('label', models.CharField(max_length=63, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=63, null=True, verbose_name='name')),
                ('type', models.CharField(choices=[('DateTimeField', '日期时间'), ('DateField', '日期')], default='DateTimeField', max_length=50, verbose_name='类型')),
                ('default_now', models.BooleanField(default=False, verbose_name='默认为当前时间')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '日期字段',
                'verbose_name_plural': '日期字段',
            },
        ),
        migrations.CreateModel(
            name='DicDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('value', models.CharField(max_length=255, verbose_name='值')),
                ('diclist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define.diclist', verbose_name='字典')),
                ('icpc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='define_icpc.icpc', verbose_name='ICPC')),
            ],
            options={
                'verbose_name': '业务字典明细',
                'verbose_name_plural': '业务字典明细',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(('app_label', 'define'), models.Q(('model', 'characterfield'), ('model', 'numberfield'), ('model', 'dtfield'), ('model', 'relatedfield'), _connector='OR')), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': '业务字段汇总',
                'verbose_name_plural': '业务字段汇总',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CharacterField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('label', models.CharField(max_length=63, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=63, null=True, verbose_name='name')),
                ('type', models.CharField(choices=[('CharField', '单行文本'), ('TextField', '多行文本')], default='CharField', max_length=50, verbose_name='类型')),
                ('length', models.PositiveSmallIntegerField(default=255, verbose_name='字符长度')),
                ('default', models.CharField(blank=True, max_length=255, null=True, verbose_name='默认值')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '字符字段',
                'verbose_name_plural': '字符字段',
            },
        ),
    ]
