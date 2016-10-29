from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from .models import Tag
from .forms import AddTagForm

# Create your views here.


def tag_list(request):
    tags = get_list_or_404(Tag.objects.filter(deleted=False))
    return render(request, "tag_manage/tag_list.html",
                  {'tag_list': tags})


def add_list(request):
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            tag = Tag()
            tag.tag_name = form.data.get('tag_name')
            tag.priority = form.data.get('priority')
            tag.save()
            return HttpResponseRedirect('/tag')
    else:
        form = AddTagForm()
    return render(request, 'tag_manage/add_tag.html', {'form': form})
