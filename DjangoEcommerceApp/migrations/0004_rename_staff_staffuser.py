# Generated by Django 4.1 on 2022-09-03 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoEcommerceApp', '0003_merchantuser_is_added_by_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Staff',
            new_name='StaffUser',
        ),
    ]
