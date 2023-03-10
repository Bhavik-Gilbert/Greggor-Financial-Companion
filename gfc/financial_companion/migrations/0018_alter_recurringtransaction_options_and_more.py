# Generated by Django 4.1.3 on 2023-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0017_alter_transaction_receiver_account_and_more'),
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
            name='interval',
            field=models.CharField(
                choices=[
                    ('day',
                     'Day'),
                    ('week',
                     'Week'),
                    ('month',
                     'Month'),
                    ('year',
                     'Year')],
                max_length=10),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='LinkRecurringTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('recurring_transaction',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='financial_companion.recurringtransaction')),
                ('transaction',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='financial_companion.transaction')),
            ],
        ),
    ]
