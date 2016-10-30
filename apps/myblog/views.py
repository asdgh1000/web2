from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from .forms import UploadBlogForm, AddBlogTagForm
from ..base.utils import *
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


@permission_required('myblog.blog_info.add', login_url='/user/login')
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
            site_map_add_url("http://blog.hellowood.net/blog_detail/%d" % blog_info.id)

            return HttpResponseRedirect("/blog_detail/%d" % blog_info.id)
    else:
        form = UploadBlogForm()
    return render(request, 'myblog/upload_blog.html', {'form': form})


def blog_detail(request, blog_info_id):
    blog_info = get_object_or_404(BlogInfo, pk=blog_info_id)
    blog_file_path = os.path.join(BLOG_FILE_PATH, blog_info.file_path)
    blog_content = read_file_to_string(blog_file_path)
    tags = BlogTagRelation.objects.filter(deleted=False).filter(blog_info_id=blog_info.id)
    return render(request, 'myblog/blog_detail.html',
                  {'blog':
                       {'title': blog_info.title,
                        'content': blog_content,
                        'cover_img': blog_info.cover_img,
                        'favor_count': blog_info.favor_count,
                        'dislike_count': blog_info.dislike_count,
                        'blog_info_id': blog_info_id,
                        'url': request.get_full_path(),
                        'tags': tags
                        }
                   })


def blog_list(request):

    if 'tag' in request.GET:
        blog_info_list = BlogInfo.objects.order_by("-created").\
            filter(blogtagrelation__tag_id=request.GET['tag'])
    else:
        blog_info_list = BlogInfo.objects.order_by("-created")

    paginator = Paginator(blog_info_list, 25)  # Show 25 contacts per page

    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1

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


@permission_required("myblog.blog_tag_relation.add", login_url="/user/login")
def add_blog_tag(request):
    if request.method == 'POST':
        form = AddBlogTagForm(request.POST)
        if form.is_valid():
            blog_id = request.POST['blog_id']
            tag_ids = request.POST.getlist('tags')
            tags = Tag.objects.filter(deleted=False).filter(blogtagrelation__blog_info_id=blog_id)
            tag_old_ids = [x.id for x in tags]
            for tag_new_id in tag_ids:
                if tag_new_id not in tag_old_ids:
                    BlogTagRelation(tag_id=tag_new_id, blog_info_id=blog_id).save()

            return HttpResponseRedirect("/blog_detail/%d" % blog_id)
    else:
        if 'blog_id' not in request.GET:
            raise Http404("需要博客id!")
        blog_id = request.GET['blog_id']
        tags = Tag.objects.filter(deleted=False).filter(blogtagrelation__blog_info_id=blog_id)
        tag_ids = [x.id for x in tags]
        form = AddBlogTagForm(initial={"tags": tag_ids, "blog_id": blog_id})
    return render(request, 'myblog/add_blog_tag.html', {'form': form})


def blog_edit(request):
    return render(request, 'myblog/blog_edit.html')
