# Generated by Django 5.0.6 on 2024-11-07 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_vote_council_vote_polling_booth_vote_polling_station'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('candidate', 'voter')},
        ),
    ]
