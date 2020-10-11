from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	watchlist = models.ManyToManyField('Auction_Listings', blank=True, related_name = "watched_by")
	pass


class Auction_Listings(models.Model):
	FASHION = 'FA'
	TOYS = 'TO'
	ELECTRONICS = 'EL'
	HOME = 'HO'
	BOOKS = 'BO'

	CATEGORY_CHOICES = [
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (BOOKS, 'Books'),
    ]
	auto_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
	title = models.CharField(max_length = 200)
	description = models.TextField()
	initial_bid = models.DecimalField(max_digits=6, decimal_places=2)
	url = models.URLField(max_length = 200)
	category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=FASHION,
    )
	closed = models.BooleanField(default=False)
	

	def __str__(self):
		return f"{self.title}, bid : {self.initial_bid}"

class Bid(models.Model):
	bid_price = models.DecimalField(max_digits=6, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE, related_name="bids")	
	pass

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE, related_name="comments")	
	comment = models.TextField()
	pass