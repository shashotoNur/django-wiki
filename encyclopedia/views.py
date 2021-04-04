from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import markdown as md
import random

# Create your views here.

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request,title):
    if util.get_entry(title):
        content=util.get_entry(title)

        return render(request,"encyclopedia/content.html", {
            "title": title.upper(),
            "content":md.markdown(content)
        })

    else:
        return render(request,"encyclopedia/error.html")


def search(request):
    query = request.POST.get("q")
    entries = []

    if util.get_entry(query):
        return redirect('title',title = query)

    else:
        all_entries = util.list_entries()

        for entry in all_entries:
            query_as_lower = str(query).lower()
            entry = str(entry).lower()
            if(entry.find(query_as_lower)!= -1):
                entries.append(entry)

        if len(entries ) == 0:
            return render(request,"encyclopedia/error.html")
        else:
            return render(request, "encyclopedia/search.html", {
        "entries": entries 
    })


def randompage(request):
    all_entries = util.list_entries()
    upper_limit = (len(all_entries) - 1)
    i = random.randint(0, upper_limit)
    return redirect('title', title = all_entries[i])


def create(request):
    if request.method == "GET":
        return render(request,"encyclopedia/create.html")

    elif request.method == "POST":
        title = request.POST.get("title")
        markdown = request.POST.get("markdown")
        content = f"# {title} \n {markdown}"
        
        if util.get_entry(title):
            return render(request,"encyclopedia/pageexists.html", {
                "entry":title
            })

        else:
            util.save_entry(title, content)
            return redirect('title', title=title)


def edit(request, title):
    if request.method == "GET":
        return render(request,"encyclopedia/edit.html", {
            "title":title.capitalize(),
            "content":util.get_entry(title)
        })
    
    elif request.method == "POST":
        content = request.POST.get("markdown")
        capitalized_title = title.capitalize()

        util.save_entry(capitalized_title, content)

        return redirect('title', title=capitalized_title)
