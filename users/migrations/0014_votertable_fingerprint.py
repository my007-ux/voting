# Generated by Django 5.0.6 on 2024-11-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_transactionpart1_transactionpart2_transactionpart3'),
    ]

    operations = [
        migrations.AddField(
            model_name='votertable',
            name='fingerprint',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
