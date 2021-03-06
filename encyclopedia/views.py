from django.shortcuts import render, redirect
from . import util
from markdown2 import markdown
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = title + " DOES NOT EXIST"
    if util.get_entry(title) is not None:
        content = markdown(util.get_entry(title))

    if "history" not in request.session:
        request.session["history"] = []
    request.session["history"] += [title]

    return render(request, "encyclopedia/page.html", {
        "name": title,
        "content": content
    })


def search(request):
    t = request.GET.get('q', ' ')
    tmp = util.list_entries()
    if t in util.list_entries():
        return entry(request, t)
    entries = []
    for e in tmp:
        if t in e.lower():
            entries.append(e)
    return render(request, "encyclopedia/listSearch.html", {
        "entries": entries
    })


def history(request):
    if "history" not in request.session:
        request.session["history"] = []
    return render(request, "encyclopedia/history.html", {
        "entries": request.session["history"]
    })


def saveEntry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title == "" or content == "":
            return render(request, "encyclopedia/saveEntry.html", {
                "message": "Can't save with empty fields.",
                "title": title,
                "content": content
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/saveEntry.html", {
                "message": "Title already exists.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return entry(request, title)
    return render(request, "encyclopedia/saveEntry.html", {})


def editEntry(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        content = request.POST.get("content")
        title = request.POST.get("title")
        if content == "":
            return render(request, "encyclopedia/editEntry.html", {
                "message": "Can't save with empty field.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return entry(request, title)
    return render(request, "encyclopedia/editEntry.html", {
        "title": title,
        "content": content
    })


def deletePage(request, title):
    util.delete_entry(title)
    return render(request, "encyclopedia/delete.html", {
        "title": title
    })


def randomPage(request):
    pages = util.list_entries()
    size = len(pages)
    rand = randint(0, size - 1)
    return entry(request, pages[rand])


def home(request):
    content = markdown(util.get_entry("Wiki Clone"))
    return render(request, "encyclopedia/Home.html", {
        "content": content
    })
