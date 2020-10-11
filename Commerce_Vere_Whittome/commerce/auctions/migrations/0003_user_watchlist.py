# Generated by Django 3.1.1 on 2020-10-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listings_bids_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watched_by', to='auctions.Auction_Listings'),
        ),
    ]