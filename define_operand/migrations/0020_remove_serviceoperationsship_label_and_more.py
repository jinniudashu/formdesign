# Generated by Django 4.0 on 2022-03-10 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_operand', '0019_serviceoperationsship_label_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceoperationsship',
            name='label',
        ),
        migrations.RemoveField(
            model_name='serviceoperationsship',
            name='name',
        ),
        migrations.RemoveField(
            model_name='servicepackageservicesship',
            name='label',
        ),
        migrations.RemoveField(
            model_name='servicepackageservicesship',
            name='name',
        ),
    ]
