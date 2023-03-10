# Generated by Django 4.1.3 on 2023-01-20 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[
                 ('income', 'Income'), ('expense', 'Expense')], max_length=7)),
                ('timespan', models.CharField(choices=[
                 ('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], max_length=5)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency',
                 models.CharField(choices=[('USD',
                                            'Unitedstatesdollar'),
                                           ('GBP',
                                            'Britishpound'),
                                           ('EUR',
                                            'Euro')],
                                  default='GBP',
                                  max_length=5)),
                ('category_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='financial_companion.category')),
            ],
            options={
                'unique_together': {('transaction_type', 'timespan', 'category_id')},
            },
        ),
    ]
