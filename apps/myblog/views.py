from django.shortcuts import render, render_to_response
from .forms import UploadFileForm
from ..base.utils import save_file
import os


# Create your views here.
def index(request):
    context = {
        "title": "Hello Wood!",
        "body": "你好，wood！"
    }
    return render(request, 'myblog/index.html', context)


def upload_blog(request):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/blog_file')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        blog_fd = form.file
        file_name = form.file_name
        if form.is_valid():
            save_file(blog_fd, base_path + file_name)
            context = {
                "title": "Hello Wood!",
                "body": "你好，wood！"
            }
            return render(request, 'myblog/index.html', context)
    else:
        form = UploadFileForm()
    return render_to_response('myblog/upload_blog.html', {'form': form})
