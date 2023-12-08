# Generated by Django 4.0.6 on 2022-08-25 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_alter_sequencestorage_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='completition',
            name='origin_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='completitions', to='documents.invoice', verbose_name='Origin Invoice'),
        ),
    ]