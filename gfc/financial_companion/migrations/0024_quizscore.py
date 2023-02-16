# Generated by Django 4.1.3 on 2023-02-16 20:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial_companion', '0023_quizset'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_questions', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('correct_questions', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('time_of_submission', models.DateTimeField(auto_now_add=True)),
                ('quiz_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_companion.quizset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time_of_submission'],
            },
        ),
    ]
