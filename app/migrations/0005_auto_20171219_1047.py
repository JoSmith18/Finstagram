# Generated by Django 2.0 on 2017-12-19 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='document',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
