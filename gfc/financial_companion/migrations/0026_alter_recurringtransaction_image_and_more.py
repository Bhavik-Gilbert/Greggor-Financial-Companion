# Generated by Django 4.1.3 on 2023-02-24 14:14

from django.db import migrations, models
import financial_companion.models.transaction_models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0025_merge_0023_merge_20230212_1250_0024_quizscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringtransaction',
            name='image',
            field=models.ImageField(
                blank=True,
                upload_to=financial_companion.models.transaction_models.change_filename),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='image',
            field=models.ImageField(
                blank=True,
                upload_to=financial_companion.models.transaction_models.change_filename),
        ),
    ]
