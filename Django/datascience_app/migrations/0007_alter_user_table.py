# Generated by Django 5.0.8 on 2024-09-03 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datascience_app', '0006_rename_users_user'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='users.Users',
        ),
    ]
