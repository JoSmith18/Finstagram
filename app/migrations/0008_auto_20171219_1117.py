# Generated by Django 2.0 on 2017-12-19 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='image',
            new_name='video',
        ),
    ]