# Generated by Django 4.0 on 2023-04-12 13:20

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0001_initial'),
        ('define_operand', '0004_alter_computecomponentssetting_component'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computecomponentssetting',
            name='js_script',
        ),
        migrations.AlterField(
            model_name='computecomponentssetting',
            name='component',
            field=models.ForeignKey(limit_choices_to=models.Q(('formcomponentssetting__form', django.db.models.expressions.F('formcomponentssetting__form'))), on_delete=django.db.models.deletion.CASCADE, to='define.component', verbose_name='字段'),
        ),
    ]
