# Generated by Django 4.1.3 on 2023-10-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0005_bankaccount_currency"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bankaccount",
            options={"ordering": ["-id"]},
        ),
        migrations.AddField(
            model_name="bankaccount",
            name="actual",
            field=models.BooleanField(default=False, verbose_name="Actual account"),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="currency",
            field=models.CharField(
                choices=[
                    ("UAH", "грн."),
                    ("EUR", "Euro"),
                    ("USD", "US Dollar"),
                    ("CHF", "CHF"),
                ],
                default="UAH",
                max_length=3,
            ),
        ),
    ]