# Generated by Django 4.0 on 2022-03-26 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0010_eventrule_intervalrule_and_more'),
        ('define_rule_dict', '0003_delete_servicespec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventexpression',
            name='event_rule',
        ),
        migrations.RemoveField(
            model_name='eventexpression',
            name='field',
        ),
        migrations.DeleteModel(
            name='IntervalRule',
        ),
        migrations.DeleteModel(
            name='EventExpression',
        ),
        migrations.DeleteModel(
            name='EventRule',
        ),
    ]
