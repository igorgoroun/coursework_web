# Generated by Django 4.0.4 on 2022-07-28 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_alter_bankaccount_iban'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='UAH', max_length=3),
        ),
    ]
