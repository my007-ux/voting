# Generated by Django 5.0.6 on 2024-11-24 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_votertable_fingerprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votertable',
            name='fingerprint',
            field=models.CharField(max_length=200),
        ),
    ]