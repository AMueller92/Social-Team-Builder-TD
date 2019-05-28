# Generated by Django 2.2 on 2019-05-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190508_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='accounts.Skill'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(blank=True, choices=[('PY', 'Python'), ('JV', 'Java'), ('JS', 'JavaScript'), ('PHP', 'Php'), ('RU', 'Ruby')], default='', max_length=50),
        ),
    ]