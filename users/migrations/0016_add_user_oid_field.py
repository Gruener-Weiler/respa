# Generated by Django 2.2.18 on 2021-03-08 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200724_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='oid',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Oid'),
        ),
    ]