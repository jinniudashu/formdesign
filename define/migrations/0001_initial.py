# Generated by Django 4.0 on 2022-04-08 14:46

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
            name='RelateFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('related_content', models.CharField(blank=True, max_length=100, null=True, verbose_name='关联内容')),
                ('related_content_type', models.CharField(choices=[('diclist', '基础字典'), ('icpclist', 'ICPC'), ('managedentity', '管理实体')], default=0, max_length=20, verbose_name='关联内容类型')),
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
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('type', models.CharField(choices=[('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')], default='ChoiceField', max_length=50, verbose_name='类型')),
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
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('type', models.CharField(choices=[('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')], default='IntegerField', max_length=50, verbose_name='类型')),
                ('max_digits', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='最大位数')),
                ('decimal_places', models.PositiveSmallIntegerField(blank=True, default=2, null=True, verbose_name='小数位数')),
                ('standard_value', models.FloatField(blank=True, null=True, verbose_name='标准值')),
                ('up_limit', models.FloatField(blank=True, null=True, verbose_name='上限')),
                ('down_limit', models.FloatField(blank=True, null=True, verbose_name='下限')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='单位')),
                ('default', models.FloatField(blank=True, null=True, verbose_name='默认值')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
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
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('type', models.CharField(choices=[('DateTimeField', '日期时间'), ('DateField', '日期')], default='DateTimeField', max_length=50, verbose_name='类型')),
                ('default_now', models.BooleanField(default=False, verbose_name='默认为当前时间')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
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
            name='ComponentsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('components', models.ManyToManyField(to='define.Component', verbose_name='字段')),
            ],
            options={
                'verbose_name': '组件',
                'verbose_name_plural': '组件',
            },
        ),
        migrations.CreateModel(
            name='CharacterField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('type', models.CharField(choices=[('CharField', '单行文本'), ('TextField', '多行文本')], default='CharField', max_length=50, verbose_name='类型')),
                ('length', models.PositiveSmallIntegerField(default=255, verbose_name='字符长度')),
                ('required', models.BooleanField(default=False, verbose_name='必填')),
                ('default', models.CharField(blank=True, max_length=255, null=True, verbose_name='默认值')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '字符字段',
                'verbose_name_plural': '字符字段',
            },
        ),
    ]
