from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        "title": "Hello Wood!"
    }
    return render(request, 'mainSite/index.html', context)
