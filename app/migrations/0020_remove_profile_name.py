# Generated by Django 2.0 on 2018-01-04 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_profile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]
