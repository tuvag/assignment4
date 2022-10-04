from django.shortcuts import render
from django import forms
import random
import markdown2

from . import util

class FormSearch(forms.Form):
    search = forms.CharField(max_length=100)

class CreateEntry(forms.Form):
    title = forms.CharField(label= "Add title here")
    content = forms.CharField(label="Add content here", widget=forms.Textarea)

class EditEntry(forms.Form):
    title = forms.CharField(label= "Edit title")
    body = forms.CharField(label= "Edit content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    entry = util.get_entry(title)
    if entry is None:
        form = FormSearch()
        errormsg = "We could not find the page you are looking for."
        return render(request, "encyclopedia/error.html", {"form": form, "content": errormsg})
    else:
        form = FormSearch()
        return render(request, "encyclopedia/entry.html", {"form":form, "content": entry, "title": title})
    

def search(request, input):
    return

def random_page(request):
    pages = util.list_entries()
    length = len(pages)
    number = random.randint(0, length-1)
    title = pages[number]
    raw_page = util.get_entry(title)
    html_page = markdown2.markdown(raw_page)
    form = FormSearch()
    return render(request, "encyclopedia/random_page.html", {"form": form, "title": title, "content": html_page})


