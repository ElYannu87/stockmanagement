# Generated by Django 3.2 on 2021-04-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0002_alter_stock_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='item_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
