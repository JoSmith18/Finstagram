# Generated by Django 2.0 on 2018-01-04 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
    ]
