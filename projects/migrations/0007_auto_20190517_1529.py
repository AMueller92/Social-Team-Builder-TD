# Generated by Django 2.2.1 on 2019-05-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20190517_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='length',
            field=models.IntegerField(),
        ),
    ]