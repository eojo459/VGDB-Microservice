# Generated by Django 5.0.7 on 2024-10-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('requirements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='requirements',
            field=models.ManyToManyField(blank=True, to='requirements.requirements'),
        ),
    ]
