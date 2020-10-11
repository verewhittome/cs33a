from django.contrib import admin

from .models import Auction_Listings, User, Bid, Comment

# Register your models here. 
admin.site.register(Auction_Listings)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)