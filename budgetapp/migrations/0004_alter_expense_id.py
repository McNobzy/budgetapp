# Generated by Django 4.0.4 on 2022-08-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0003_expense_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
