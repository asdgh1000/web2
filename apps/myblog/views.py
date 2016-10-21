from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404
from .forms import UploadFileForm
from ..base.utils import save_file
import os


# Create your views here.
def index(request):
    return render(request, 'myblog/index.html')


def upload_blog(request):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/blog_file')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            blog_fd = request.FILES['file']
            file_name = form.file_name
            save_file(blog_fd, base_path + file_name)
            return HttpResponseRedirect('myblog/index.html')
        else:
            raise Http404("表单验证失败")

    else:
        form = UploadFileForm()
    return render_to_response('myblog/upload_blog.html', {'form': form})
