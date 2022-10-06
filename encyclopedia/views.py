from django.shortcuts import redirect, render
from django import forms
import random
import markdown2
from django.contrib import messages

from . import util

class FormSearch(forms.Form):
    search = forms.CharField(max_length=100)

class CreateEntry(forms.Form):
    title = forms.CharField(label= "Add title here")
    content = forms.CharField(label="Add content here", widget=forms.Textarea(attrs={'rows': 15, 'cols': 50}))

class EditEntry(forms.Form):
    title = forms.CharField(label= "Edit title")
    content = forms.CharField(label= "Edit content", widget=forms.Textarea(attrs={'rows': 15, 'cols': 50}))

def index(request):
    form = FormSearch()
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
        raw_content = util.get_entry(title)
        content = markdown2.markdown(raw_content)
        return render(request, "encyclopedia/article.html", {"form":form, "content": content, "title": title})
    

def search(request):
    if request.method == "POST":
        form = FormSearch(request.POST) 
        if form.is_valid():
            input = form.cleaned_data.get("search")
            search_list= []
            for article in util.list_entries():
                if input == article:
                    raw_content = util.get_entry(article)
                    content = markdown2.markdown(raw_content)
                    return render(request, "encyclopedia/article.html", {"form":form, "content":content, "title": article})
                if input in article:
                    search_list.append(input)
            if len(search_list) > 0:
                return render(request, "encyclopedia/index.html", {"form":form, "entries":search_list})
            else:
                form = FormSearch()
                msg= f'Cannot find the entry you are looking for.'
                return render(request, "encyclopedia/error.html", {"form":form, "content":msg})
    else:
        form = FormSearch()
        msg = f'Search to see results'
        return render(request, "encyclopedia/error.html", {"form":form, "content":msg})


def edit_page(request, title):
    if request.method == "POST":
        edit = EditEntry(request.POST)
        if edit.is_valid():
            title = edit.cleaned_data.get("title")
            raw_content = edit.cleaned_data.get("content")
            util.save_entry(title, raw_content)
            form = FormSearch()
            content = markdown2.markdown(raw_content)
            return render(request, "encyclopedia/article.html", {"title": title, "content": content, "form": form})
    else:
        form = FormSearch()
        content = util.get_entry(title)
        edit_form = EditEntry({"title": title, "content": content})
        return render(request, "encyclopedia/edit_page.html", {"form": form, "edit_form": edit_form})


def new_page(request):
    if request.method == "POST":
        form = CreateEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            exsist = False
            for article in util.list_entries():
                if article == title:
                    exsist = True
            if not exsist:
                util.save_entry(title, content)
                form = FormSearch()
                raw_content = util.get_entry(title)
                content = markdown2.markdown(raw_content)
                messages.success(request, f'New aritcle was added')
                return render(request, "encyclopedia/article.html", {"form": form, "title":title, "content":content})
            else:
                em = f'Article already exists'
                messages.error(request, em)
                return redirect("error")
    else:
        form = FormSearch()
        new = CreateEntry()
        return render(request, "encyclopedia/new_page.html", {"form": form, "new_form": new})


def error(request):
    msg = f'Something went wrong'
    return render(request, "encyclopedia/error.html", {"errormsg": msg})

def random_page(request):
    pages = util.list_entries()
    length = len(pages)
    number = random.randint(0, length-1)
    title = pages[number]
    raw_page = util.get_entry(title)
    html_page = markdown2.markdown(raw_page)
    form = FormSearch()
    return render(request, "encyclopedia/random_page.html", {"form": form, "title": title, "content": html_page})


