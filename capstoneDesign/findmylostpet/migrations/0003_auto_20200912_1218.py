# Generated by Django 3.0.6 on 2020-09-12 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findmylostpet', '0002_findlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='Photo',
            field=models.FileField(default='', upload_to='../capstone/media/lostList/images'),
        ),
    ]