# Generated by Django 2.0 on 2017-12-19 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20171219_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='posted_by',
            field=models.CharField(default='The Owner', max_length=16),
            preserve_default=False,
        ),
    ]