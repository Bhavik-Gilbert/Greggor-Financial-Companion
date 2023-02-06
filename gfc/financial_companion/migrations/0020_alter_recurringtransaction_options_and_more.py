# Generated by Django 4.1.3 on 2023-02-06 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0019_merge_20230206_1440'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recurringtransaction',
            options={'ordering': ['-interval']},
        ),
        migrations.AlterUniqueTogether(
            name='recurringtransaction',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financial_companion.category'),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='currency',
            field=models.CharField(choices=[('GBP', 'Gbp'), ('USD', 'Usd'), ('EUR', 'Eur'), ('JPY', 'Jpy'), ('CNY', 'Cny'), ('AUD', 'Aud'), ('CAD', 'Cad'), ('INR', 'Inr'), ('RUB', 'Rub'), ('NZD', 'Nzd'), ('CHF', 'Chf'), ('KZT', 'Kzt')], max_length=3),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='interval',
            field=models.CharField(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], max_length=10),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
