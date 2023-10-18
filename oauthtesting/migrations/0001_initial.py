# Generated by Django 4.2.6 on 2023-10-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('points', models.IntegerField(default=0)),
                ('bio', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to='images')),
            ],
        ),
    ]