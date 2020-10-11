from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
	path("new_page", views.new_page, name="new_page"),
	path("edit/<str:edit_name>", views.edit, name="edit"),
	path("random" , views.random_entry, name="random"),
	path("<str:entry_name>", views.entry, name="entry"),


]
