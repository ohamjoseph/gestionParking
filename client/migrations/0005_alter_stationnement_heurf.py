# Generated by Django 4.0.4 on 2022-04-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_stationnement_date_alter_stationnement_heurd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationnement',
            name='heurF',
            field=models.TimeField(blank=True, null=True),
        ),
    ]