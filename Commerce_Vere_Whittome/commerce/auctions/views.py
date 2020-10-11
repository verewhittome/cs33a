from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


from .models import User
from auctions.models import Auction_Listings, Bid, Comment


def index(request):
	listings = Auction_Listings.objects.all()
	bids = Bid.objects.all()
	return render(request, "auctions/index.html", {
	"listings" : listings,
	"categories": Auction_Listings.CATEGORY_CHOICES
	})

def watchlist(request):
	user = User.objects.get(username=request.user.username)
	watchlist = user.watchlist.all()
	return render(request, "auctions/watchlist.html", {
	"watchlist" : watchlist
	})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



		
def new_listing(request):
	return render(request, "auctions/new_listing.html", {
		"categories": Auction_Listings.CATEGORY_CHOICES
	})


def add_listing(request):
	if request.method == "POST":
		if request.user.is_authenticated:

			title = request.POST["title"]
			description = request.POST["description"]
			bid_price = request.POST["bid_price"]
			url = request.POST["url"]
			category = request.POST["category"]

			listing = Auction_Listings(user = request.user, title = title, description = description, initial_bid = bid_price, url=url, category=category)
			listing.save()
		
	return render(request, "auctions/new_listing.html", {
		"categories": Auction_Listings.CATEGORY_CHOICES
	})


def listing_view(request, listing_id):
	listing = Auction_Listings.objects.get(pk=listing_id)
	watchlist = listing.watched_by.all()
	comments = listing.comments.all()
	try:

		bid = Bid.objects.get(listing=listing)
	except:
		bid = False
		
	return render(request, "auctions/listing.html", {
		"listing": listing,
		"watchlist": watchlist,
		"bid": bid,
		"comments": comments,
		"categories": Auction_Listings.CATEGORY_CHOICES
	})
		


def add_to_watchlist(request):
	if request.user.is_authenticated:	
		if request.method == 'POST':
			listing_id = request.POST["listing_id"]
			
			listing = Auction_Listings.objects.get(pk=listing_id)
			user = User.objects.get(username=request.user.username)

			user.watchlist.add(listing)

	return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.pk}))

def remove_from_watchlist(request):
	if request.user.is_authenticated:	
		if request.method == 'POST':
			listing_id = request.POST["listing_id"]
			print(listing_id)
			listing = Auction_Listings.objects.get(pk=listing_id)
			user = User.objects.get(username=request.user.username)
			print(user)			
			user.watchlist.remove(listing)

	return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.pk}))

def close_listing(request):
	if request.user.is_authenticated:	
		if request.method == 'POST':
			listing_id = request.POST["listing_id"]
			listing = Auction_Listings.objects.get(pk=listing_id)
			listing.closed = True
			listing.save()
	return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.pk}))

def submit_bid(request):
	if request.user.is_authenticated:	
		if request.method == 'POST':
			listing_id = request.POST["listing_id"]
			bid_price = float(request.POST["bid_price"])
			listing = Auction_Listings.objects.get(pk=listing_id)

			try:

				bid = Bid.objects.get(listing=listing)

				if bid_price > bid.bid_price:
					bid.bid_price = bid_price
					bid.save()
				else:
					messages.error(request, 'Please enter a bid higher than the current')

			except Bid.DoesNotExist:
				
				if bid_price > listing.initial_bid:
					bid = Bid(bid_price=bid_price, user=request.user, listing=listing)
					bid.save()
				else:
					messages.error(request, 'Please enter a bid higher than the current')
					
	return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.pk}))


def write_comment(request):
	if request.user.is_authenticated:	
		if request.method == 'POST':
			listing_id = request.POST["listing_id"]
			comment = request.POST["comment"]
			listing = Auction_Listings.objects.get(pk=listing_id)
			comment = Comment(comment=comment, user=request.user, listing=listing)
			comment.save()
	return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.pk}))			
			
	
def category_list(request):
	return render(request, "auctions/category_list.html", {
	"categories": Auction_Listings.CATEGORY_CHOICES
	})

def category(request, category):
	category_list = Auction_Listings.objects.filter(category=category)
	return render(request, "auctions/category.html", {
	"categories": Auction_Listings.CATEGORY_CHOICES,
	"category_list": category_list
	})
	

		