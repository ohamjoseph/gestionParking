# Generated by Django 4.0.4 on 2022-04-19 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_remove_stationnement_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationnement',
            name='dateD',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='stationnement',
            name='dateF',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
