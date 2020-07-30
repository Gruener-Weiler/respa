# Generated by Django 2.2.5 on 2020-02-05 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('respa_outlook', '0001_initial'),
        ('resources', '0111_auto_20200127_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='configuration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Configuration', to='respa_outlook.RespaOutlookConfiguration', verbose_name='Outlook configuration'),
        ),
    ]