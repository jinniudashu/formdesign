# Generated by Django 4.0 on 2022-01-01 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0005_inquireform_fields_mutateform_fields_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operandview',
            old_name='fields',
            new_name='mutate_fields',
        ),
    ]
