# Generated by Django 3.0.8 on 2020-07-28 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0009_auto_20200728_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='', upload_to='company_images'),
            preserve_default=False,
        ),
    ]
