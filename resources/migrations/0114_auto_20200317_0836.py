# Generated by Django 2.2.10 on 2020-03-17 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0113_auto_20200206_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='payment_terms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources_where_payment_terms', to='resources.TermsOfUse', verbose_name='Payment terms'),
        ),
        migrations.AddField(
            model_name='termsofuse',
            name='terms_type',
            field=models.CharField(choices=[('payment_terms', 'Payment terms'), ('generic_terms', 'Generic terms')], default='generic_terms', max_length=40, verbose_name='Terms type'),
        ),
        migrations.AlterField(
            model_name='accessibilityvalue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='accessibilityvalue',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time of modification'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time of modification'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='name_fi',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='name_sv',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='accessibilityviewpoint',
            name='order_text',
            field=models.CharField(default='0', max_length=200, verbose_name='Järjestys'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='generic_terms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources_where_generic_terms', to='resources.TermsOfUse', verbose_name='Generic terms'),
        ),
        migrations.AlterField(
            model_name='resourceaccessibility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='resourceaccessibility',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time of modification'),
        ),
        migrations.AlterField(
            model_name='resourceaccessibility',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessibility_summaries', to='resources.Resource', verbose_name='Resource'),
        ),
        migrations.AlterField(
            model_name='unitaccessibility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='unitaccessibility',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time of modification'),
        ),
        migrations.AlterField(
            model_name='unitaccessibility',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessibility_summaries', to='resources.Unit', verbose_name='Resource'),
        ),
    ]
