# Generated by Django 4.2.14 on 2024-07-26 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_listing_watchlist_listings_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
