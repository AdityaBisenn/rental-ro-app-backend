# Generated by Django 5.0.3 on 2024-06-06 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='device',
            new_name='chip',
        ),
    ]
