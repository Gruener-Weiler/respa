# Generated by Django 2.2.16 on 2021-02-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sap_code',
            field=models.CharField(blank=True, max_length=255, verbose_name='sap code'),
        ),
    ]