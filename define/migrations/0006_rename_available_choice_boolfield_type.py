# Generated by Django 4.0 on 2021-12-14 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define', '0005_alter_boolfield_default'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boolfield',
            old_name='available_choice',
            new_name='type',
        ),
    ]
