# Generated by Django 4.2.6 on 2023-11-12 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthtesting', '0023_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
