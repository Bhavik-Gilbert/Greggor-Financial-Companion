# Generated by Django 4.1.3 on 2023-01-21 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("financial_companion", "0003_account"),
    ]

    operations = [
        migrations.CreateModel(
            name="PotAccount",
            fields=[
                (
                    "account_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="financial_companion.account",
                    ),
                ),
                ("balance", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("gbp", "Gbp"),
                            ("usd", "Usd"),
                            ("eur", "Eur"),
                            ("jpy", "Jpy"),
                            ("cny", "Cny"),
                            ("aud", "Aud"),
                            ("cad", "Cad"),
                            ("kzt", "Kzt"),
                            ("inr", "Inr"),
                            ("rub", "Rub"),
                            ("nzd", "Nzd"),
                            ("chf", "Chf"),
                        ],
                        default="gbp",
                        max_length=3,
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("financial_companion.account",),
        ),
    ]
