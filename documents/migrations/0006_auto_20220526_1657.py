# Generated by Django 3.2.6 on 2022-05-26 13:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20201226_1932'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0005_auto_20210803_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('customer_invoice', 'Issued by me for customer'), ('vendor_bill', 'Received from vendor')], default='customer_invoice', max_length=16, verbose_name='Invoice direction')),
                ('number', models.CharField(max_length=128, verbose_name='Invoice number')),
                ('reference', models.CharField(blank=True, max_length=128, verbose_name='External reference')),
                ('issue_date', models.DateField(default=django.utils.timezone.now, verbose_name='Issue date')),
                ('notes', models.TextField(blank=True, verbose_name='Com short notes')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.company', verbose_name='My side')),
                ('company_signer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='signed_invoices', to=settings.AUTH_USER_MODEL, verbose_name='Signer from my side')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_completitions', to=settings.AUTH_USER_MODEL, verbose_name='Created by user')),
            ],
            options={
                'db_table': 'invoices',
            },
        ),
        migrations.AlterField(
            model_name='contract',
            name='closing_date',
            field=models.DateField(blank=True, default=datetime.date(2022, 12, 31), verbose_name='Contract closing date'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='month',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Month'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='year',
            field=models.PositiveSmallIntegerField(default=2022, verbose_name='Year'),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_hint', models.CharField(max_length=255, verbose_name='Product description')),
                ('product_uom_hint', models.CharField(max_length=16, verbose_name='UOM hint')),
                ('qty', models.FloatField(verbose_name='Product quantity')),
                ('price', models.FloatField(verbose_name='Unit price')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='documents.invoice', verbose_name='Invoice')),
            ],
            options={
                'db_table': 'invoice_lines',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='origin_contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invoices', to='documents.contract', verbose_name='Origin Contract'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='company.partner', verbose_name='Partner side'),
        ),
    ]
