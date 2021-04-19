from django.shortcuts import render

# Create your views here.

def home(request):
    title = 'Welcome to the placeholder'
    context = {
        "title" : title,
    }
    return render(request, "home.html", context)