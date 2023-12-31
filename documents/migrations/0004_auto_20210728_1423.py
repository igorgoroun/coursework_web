# Generated by Django 3.2.5 on 2021-07-28 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20201227_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='closing_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 12, 31), verbose_name='Contract closing date'),
        ),
        migrations.AlterField(
            model_name='sequencesetup',
            name='step',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Step'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='month',
            field=models.PositiveSmallIntegerField(default=7, verbose_name='Month'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='number_for_month',
            field=models.IntegerField(default=1, verbose_name='Number in month'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='number_for_year',
            field=models.IntegerField(default=1, verbose_name='Number in year'),
        ),
        migrations.AlterField(
            model_name='sequencestorage',
            name='year',
            field=models.PositiveSmallIntegerField(default=2021, verbose_name='Year'),
        ),
        migrations.AddConstraint(
            model_name='sequencestorage',
            constraint=models.UniqueConstraint(fields=('setup', 'year', 'month'), name='uniq_setup_year_month'),
        ),
    ]
