# Generated by Django 4.1.3 on 2023-02-01 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0017_alter_accounttarget_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financial_companion.category'),
        ),
    ]
