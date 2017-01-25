from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AddTagForm
from .models import Tag
from ..base.views import render_with_public_item


# Create your views here.


def tag_list(request):
    return render_with_public_item(request, "tag_manage/tag_list.html")


@permission_required('tag_manage.tag.add', login_url='/user/login')
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
