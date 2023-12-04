# Generated by Django 4.2.6 on 2023-12-03 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthtesting', '0024_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='rejection_message',
            field=models.CharField(default='', max_length=200),
        ),
    ]
