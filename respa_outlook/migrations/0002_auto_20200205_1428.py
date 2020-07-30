# Generated by Django 2.2.5 on 2020-02-05 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0112_resource_configuration'),
        ('respa_outlook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='respaoutlookconfiguration',
            options={'verbose_name': 'Outlook configuration', 'verbose_name_plural': 'Outlook configurations'},
        ),
        migrations.CreateModel(
            name='RespaOutlookReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Reserver name & Resource')),
                ('exchange_id', models.CharField(max_length=255, verbose_name='Exchange ID')),
                ('exchange_changekey', models.CharField(max_length=255, verbose_name='Exchange Key')),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OutlookReservations', to='resources.Reservation', verbose_name='Reservation')),
            ],
            options={
                'verbose_name': 'Outlook reservation',
                'verbose_name_plural': 'Outlook reservations',
            },
        ),
    ]