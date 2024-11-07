# Generated by Django 5.0.6 on 2024-11-07 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_candidate_cnic'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='council',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.council'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='polling_booth',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.pollingbooth'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='polling_station',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.pollingstation'),
            preserve_default=False,
        ),
    ]
