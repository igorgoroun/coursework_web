# Generated by Django 4.0.4 on 2022-07-28 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0008_auto_20201226_1932'),
        ('documents', '0006_auto_20220526_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='completition',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='UAH', max_length=3, verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='contract',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='UAH', max_length=3, verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='UAH', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='completition',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.company', verbose_name='З мого боку'),
        ),
        migrations.AlterField(
            model_name='completition',
            name='number',
            field=models.CharField(max_length=128, verbose_name='Номер контракту'),
        ),
        migrations.AlterField(
            model_name='completition',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.partner', verbose_name='Із сторони партнера'),
        ),
        migrations.AlterField(
            model_name='completition',
            name='reference',
            field=models.CharField(blank=True, max_length=128, verbose_name='Зовнішний номер'),
        ),
        migrations.AlterField(
            model_name='completition',
            name='sign_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата підписання'),
        ),
        migrations.AlterField(
            model_name='completitionline',
            name='completition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='documents.completition', verbose_name='Акт виконаних робіт'),
        ),
        migrations.AlterField(
            model_name='completitionline',
            name='price',
            field=models.FloatField(verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='completitionline',
            name='product_hint',
            field=models.CharField(max_length=255, verbose_name='Найменування'),
        ),
        migrations.AlterField(
            model_name='completitionline',
            name='product_uom_hint',
            field=models.CharField(max_length=16, verbose_name='Од.виміру'),
        ),
        migrations.AlterField(
            model_name='completitionline',
            name='qty',
            field=models.FloatField(verbose_name='Кількість'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.company', verbose_name='З мого боку'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='number',
            field=models.CharField(max_length=128, verbose_name='Номер контракту'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.partner', verbose_name='Із сторони партнера'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='reference',
            field=models.CharField(blank=True, max_length=128, verbose_name='Зовнішний номер'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='sign_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата підписання'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.company', verbose_name='З мого боку'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_invoices', to=settings.AUTH_USER_MODEL, verbose_name='Created by user'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issue_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(max_length=128, verbose_name='Номер рахунку'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='company.partner', verbose_name='Із сторони партнера'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='reference',
            field=models.CharField(blank=True, max_length=128, verbose_name='Зовнішний номер'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='documents.invoice', verbose_name='Рахунок'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='price',
            field=models.FloatField(verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='product_hint',
            field=models.CharField(max_length=255, verbose_name='Найменування'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='product_uom_hint',
            field=models.CharField(max_length=16, verbose_name='Од.виміру'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='qty',
            field=models.FloatField(verbose_name='Кількість'),
        ),
        migrations.AlterField(
            model_name='sequencesetup',
            name='document',
            field=models.CharField(choices=[('invoice', 'Рахунок'), ('completition', 'Акт виконаних робіт'), ('contract', 'Договір'), ('transaction', 'Bank transaction')], max_length=32, verbose_name='Sequence type'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='month',
            field=models.PositiveSmallIntegerField(default=7, verbose_name='Month'),
        ),
    ]