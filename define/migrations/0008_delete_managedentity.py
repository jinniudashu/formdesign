# Generated by Django 4.0 on 2022-02-20 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('define_form', '0004_alter_basemodel_managed_entity_and_more'),
        ('define', '0007_remove_relatedfield_related_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ManagedEntity',
        ),
    ]
