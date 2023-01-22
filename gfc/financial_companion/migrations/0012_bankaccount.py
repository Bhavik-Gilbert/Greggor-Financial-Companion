# Generated by Django 4.1.3 on 2023-01-21 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("financial_companion", "0011_alter_transaction_time_of_transaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                (
                    "potaccount_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="financial_companion.potaccount",
                    ),
                ),
                ("bank_name", models.CharField(max_length=50)),
                ("account_number", models.CharField(max_length=8)),
                ("sort_code", models.CharField(max_length=6)),
                ("iban", models.CharField(blank=True, max_length=34)),
            ],
            bases=("financial_companion.potaccount",),
        ),
    ]