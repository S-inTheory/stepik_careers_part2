# Generated by Django 3.0.8 on 2020-07-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0007_auto_20200720_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='company_images'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='picture',
            field=models.ImageField(upload_to='speciality_images'),
        ),
    ]
