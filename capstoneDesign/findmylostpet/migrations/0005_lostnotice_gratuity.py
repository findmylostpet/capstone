# Generated by Django 3.0.6 on 2020-09-17 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findmylostpet', '0004_auto_20200917_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='lostnotice',
            name='Gratuity',
            field=models.IntegerField(null=True),
        ),
    ]