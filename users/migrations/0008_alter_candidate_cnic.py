# Generated by Django 5.0.6 on 2024-11-07 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_candidate_cnic_candidate_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='cnic',
            field=models.CharField(max_length=120),
        ),
    ]