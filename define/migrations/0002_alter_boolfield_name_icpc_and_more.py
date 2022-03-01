# Generated by Django 4.0 on 2022-03-01 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('define_icpc', '0001_initial'),
        ('define', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boolfield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
        migrations.AlterField(
            model_name='characterfield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
        migrations.AlterField(
            model_name='choicefield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
        migrations.AlterField(
            model_name='dtfield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
        migrations.AlterField(
            model_name='numberfield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
        migrations.AlterField(
            model_name='relatedfield',
            name='name_icpc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='define_icpc.icpc', verbose_name='ICPC编码'),
        ),
    ]
