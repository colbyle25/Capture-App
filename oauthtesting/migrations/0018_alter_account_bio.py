# Generated by Django 4.2.6 on 2023-11-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauthtesting", "0017_merge_20231108_0042"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="bio",
            field=models.CharField(default="A user", max_length=200),
        ),
    ]