from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
	path("new_listing", views.new_listing, name="new_listing"),
	path("add_listing", views.add_listing, name="add_listing"),
	path("category_list", views.category_list, name="category_list"),
	path("categories/<str:category>", views.category, name="category"),
	path("listing/<int:listing_id>", views.listing_view, name="listing_view"),
	path("watchlist",views.watchlist, name="watchlist"),
	path("close_listing", views.close_listing, name="close_listing"),
	path("submit_bid", views.submit_bid, name="submit_bid"),	
	path("write_comment",views.write_comment, name="write_comment"),
	path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
	path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist")
]
