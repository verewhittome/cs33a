# Generated by Django 3.1.1 on 2020-10-10 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Auction_Listings',
            fields=[
                ('auto_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('url', models.URLField()),
                ('category', models.CharField(choices=[('FA', 'Fashion'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), ('BO', 'Books')], default='FA', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]