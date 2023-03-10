# Generated by Django 4.1.3 on 2023-03-08 17:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0026_alter_recurringtransaction_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttarget',
            name='amount',
            field=models.DecimalField(
                decimal_places=2, max_digits=15, validators=[
                    django.core.validators.MinValueValidator(
                        Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='categorytarget',
            name='amount',
            field=models.DecimalField(
                decimal_places=2, max_digits=15, validators=[
                    django.core.validators.MinValueValidator(
                        Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='usertarget',
            name='amount',
            field=models.DecimalField(
                decimal_places=2, max_digits=15, validators=[
                    django.core.validators.MinValueValidator(
                        Decimal('0.01'))]),
        ),
    ]
