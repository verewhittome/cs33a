from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2


class New_Page_Form(forms.Form):
	title = forms.CharField(label="title")
	text = forms.CharField(widget=forms.Textarea, label="text")


	
def index(request):
	if request.method == 'POST':
		query_string = request.POST['query_string']
		print(query_string)
		entries = util.list_entries()
		result = [entry for entry in entries if query_string in entry]
		
		entry = util.get_entry(query_string)
		if util.get_entry(query_string):
			return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":query_string}))
		elif result:
			return render(request, "encyclopedia/index.html", {
		    "entries": result,
			"title": "Search Results",
			"heading": "Search Results"
			})
	
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries(),
		"title": "Encyclopedia",
		"heading": "All Pages"
	})


def new_page(request):
	if request.method == 'POST':
		form = New_Page_Form(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			if util.get_entry(title):
				return HttpResponse("Entry '{}' already exists".format(title))
			else:

				text = form.cleaned_data["text"]
				path_folder = "./entries"
				md_file = "{}/{}.md".format(path_folder,title)
				with open(md_file, 'w') as f:
					f.write(text)
				return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":title}))

	return render(request, "encyclopedia/new_page.html", {
        "form": New_Page_Form(),
		"title": "New Page"
		})

	
def entry(request, entry_name):
	entry = markdown2.markdown(util.get_entry(entry_name))
	if entry:
		return render(request, "encyclopedia/entry.html", {
        "entry": entry,
		"title": entry_name
		})
	else :
		return HttpResponse("Error: File not found")

		

def edit(request, edit_name):
	if request.method == 'POST':
		text = request.POST['text']
		title = edit_name
		path_folder = "./entries"
		md_file = "{}/{}.md".format(path_folder,title)
		with open(md_file, 'w') as f:
			f.write(text)
		return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":title}))

	return render(request, "encyclopedia/edit.html", {
		"entry_title": edit_name,
		"title": "Edit",
		"entry": util.get_entry(edit_name),
		})

def random_entry(request):
	entries = util.list_entries()
	random_entry = random.choice(entries)
	return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":random_entry}))
	
