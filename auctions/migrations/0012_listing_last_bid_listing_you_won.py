# Generated by Django 4.2.14 on 2024-07-26 18:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='last_bid',
            field=models.ManyToManyField(related_name='last_bid_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='you_won',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
