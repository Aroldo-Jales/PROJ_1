# Generated by Django 3.2 on 2021-07-13 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mercurium', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Limite'),
        ),
    ]
