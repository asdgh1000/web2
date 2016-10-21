from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404
from .forms import UploadBlogForm
from ..base.utils import save_file
import os


# Create your views here.
def index(request):
    return render(request, 'myblog/index.html')


def upload_blog(request):
    blog_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/blog_file/')
    if request.method == 'POST':
        form = UploadBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_fd = request.FILES['file']
            file_name = form.data.get('file_name')
            save_file(blog_fd, blog_path + file_name)
            return HttpResponseRedirect('/')
    else:
        form = UploadBlogForm()
    return render(request, 'myblog/upload_blog.html', {'form': form})
