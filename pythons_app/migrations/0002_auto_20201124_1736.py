# Generated by Django 3.1.2 on 2020-11-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythons_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='python',
            name='image',
            field=models.ImageField(upload_to='pythons'),
        ),
    ]
