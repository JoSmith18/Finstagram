# Generated by Django 2.0 on 2017-12-21 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_commentvid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentvid',
            old_name='document',
            new_name='video',
        ),
    ]
