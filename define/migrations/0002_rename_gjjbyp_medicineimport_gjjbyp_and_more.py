# Generated by Django 4.0 on 2023-08-03 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicineimport',
            old_name='gjjbyp',
            new_name='Gjjbyp',
        ),
        migrations.RenameField(
            model_name='medicineimport',
            old_name='bsyz',
            new_name='Incompatibility',
        ),
        migrations.RenameField(
            model_name='medicineimport',
            old_name='syz',
            new_name='Indications',
        ),
        migrations.RenameField(
            model_name='medicineimport',
            old_name='ybypbm',
            new_name='Ybypbm',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='AllowBreak',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='Anaphylaxis',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='CFCM',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='CFDosage',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='CountForCode',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='CurrentStorage',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='Cycle',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='EconomyBatch',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='IsSurveillant',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='IsUse',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='LastCycleDate',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='MZPrice',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='MZPriceCF',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='MaxStorage',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='Measure',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='MinBuy',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='MinStorage',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='NotCFYP',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='PricePercentLS',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='PricePercentXS',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='RK2XS',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='WJH',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='XS2CF',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='XSMeasure',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='YPSort',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='fypc',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='fytj',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='fyzysxhbz',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='isAppliance',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='isCHN',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='isNew',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='isXY',
        ),
        migrations.RemoveField(
            model_name='medicineimport',
            name='ybyplb',
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='AdverseReactions',
            field=models.CharField(max_length=255, null=True, verbose_name='不良反应'),
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='DrugAdministrationAttributes',
            field=models.CharField(max_length=60, null=True, verbose_name='药品管理属性'),
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='Frequency',
            field=models.CharField(max_length=255, null=True, verbose_name='用药频次'),
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='Note',
            field=models.CharField(max_length=255, null=True, verbose_name='用药备注'),
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='YPClass',
            field=models.CharField(max_length=60, null=True, verbose_name='药品分类'),
        ),
        migrations.AddField(
            model_name='medicineimport',
            name='Ybyplb',
            field=models.CharField(max_length=2, null=True, verbose_name='医保报销类别'),
        ),
        migrations.AlterField(
            model_name='medicineimport',
            name='CFMeasure',
            field=models.CharField(max_length=30, null=True, verbose_name='处方剂量单位'),
        ),
        migrations.AlterField(
            model_name='medicineimport',
            name='Dosage',
            field=models.CharField(max_length=60, null=True, verbose_name='常用剂量'),
        ),
        migrations.AlterField(
            model_name='medicineimport',
            name='Usage',
            field=models.CharField(max_length=60, null=True, verbose_name='用药途径'),
        ),
    ]
