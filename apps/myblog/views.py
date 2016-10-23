from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from .forms import UploadBlogForm
from ..base.utils import save_file, md5, read_file_to_string
from .settings import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os


# Create your views here.
def index(request):
    newest_bloginfo_list = BlogInfo.objects.order_by("-created")[0:5]

    newest_blog_list = []
    for blog in newest_bloginfo_list:
        newest_blog_list.append({
            'id': blog.id,
            'title': blog.title,
        })

    return render(request, 'myblog/index.html',
                  {
                      'newest_blog_list': newest_blog_list,
                  }
                  )


def upload_blog(request):
    if request.method == 'POST':
        form = UploadBlogForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.data.get('file_name')
            save_file(request.FILES['file'], os.path.join(BLOG_FILE_PATH, file_name))
            blog_info = BlogInfo()
            if 'cover_img' in request.FILES:
                img_fd = request.FILES['cover_img']
                img_name = md5(img_fd)
                save_file(img_fd, os.path.join(BLOG_COVER_PATH, img_name))
                blog_info.cover_img = img_name

            blog_info.file_path = file_name
            blog_info.title = form.data.get('title')
            blog_info.save()
            return HttpResponseRedirect('/')
    else:
        form = UploadBlogForm()
    return render(request, 'myblog/upload_blog.html', {'form': form})


def blog_detail(request, blog_info_id):
    blog_info = get_object_or_404(BlogInfo, pk=blog_info_id)
    blog_file_path = os.path.join(BLOG_FILE_PATH, blog_info.file_path)
    blog_content = read_file_to_string(blog_file_path)
    return render(request, 'myblog/blog_detail.html',
                  {'blog':
                       {'title': blog_info.title,
                        'content': blog_content,
                        'cover_img': blog_info.cover_img,
                        'favor_count': blog_info.favor_count,
                        'dislike_count': blog_info.dislike_count,
                        'blog_info_id': blog_info_id,
                        'url': request.get_full_path()
                        }
                   })


def blog_list(request, page):
    blog_info_list = BlogInfo.objects.all()
    paginator = Paginator(blog_info_list, 25)  # Show 25 contacts per page

    try:
        blog_page_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_page_list = paginator.page(paginator.num_pages)

    current_page = blog_page_list.number
    total_page = blog_page_list.paginator.num_pages
    first_page = current_page - 4 if current_page - 4 > 1 else 1
    last_page = current_page + 4 if current_page + 4 < total_page else total_page

    return render(request, 'myblog/blog_list.html',
                  {'blog_list': blog_page_list,
                   'page_range': range(first_page, last_page+1)
                   })
