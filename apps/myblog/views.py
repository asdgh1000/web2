from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django_redis import get_redis_connection

from .forms import UploadBlogForm, AddBlogTagForm, EditBlogForm
from .models import *
from .settings import *
from ..base.utils import *
from ..base.views import render_with_public_item


# Create your views here.
def index(request):
    return render_with_public_item(request, 'myblog/index.html')

def about(request):
    return render_with_public_item(request, 'myblog/about.html')


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
            blog_info.abstract = form.data.get('abstract')
            blog_info.author = request.user.username
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
    tag_relations = BlogTagRelation.objects.filter(deleted=False).filter(blog_info_id=blog_info.id)
    tags = [tag.tag for tag in tag_relations]
    redis_client = get_redis_connection()
    redis_client.incr("%s%s" % (BLOG_CLICK_PREFIX, blog_info_id))

    return render_with_public_item(request, 'myblog/blog_detail.html',
                                   {
                                       'blog': {
                                           'title': blog_info.title,
                                           'author': blog_info.author,
                                           'content': blog_content,
                                           'cover_img': blog_info.cover_img,
                                           'favor_count': blog_info.favor_count,
                                           'dislike_count': blog_info.dislike_count,
                                           'blog_info_id': blog_info_id,
                                           'url': request.get_full_path(),
                                           'tags': tags,
                                           'click_count': blog_info.click_count + 1,
                                       },
                                   })


def blog_list(request):
    if 'tag' in request.GET:
        blog_info_list = BlogInfo.objects.order_by("-created"). \
            filter(blogtagrelation__tag_id=request.GET['tag'])
    else:
        blog_info_list = BlogInfo.objects.order_by("-created")

    paginator = Paginator(blog_info_list, 5)  # Show 25 contacts per page

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

    return render_with_public_item(request, 'myblog/blog_list.html',
                                   {'blog_list': blog_page_list,
                                    'page_range': range(first_page, last_page + 1),
                                    })


@permission_required("myblog.blog_tag_relation.add", login_url="/user/login")
def add_blog_tag(request):
    if request.method == 'POST':
        form = AddBlogTagForm(request.POST)
        if form.is_valid():
            blog_id = request.POST['blog_id']
            tag_ids = request.POST.getlist('tags')
            tags = BlogTagRelation.objects.filter(deleted=False).filter(blog_info_id=blog_id)
            tag_old_ids = [x.tag_id for x in tags]
            for tag_new_id in tag_ids:
                if int(tag_new_id) not in tag_old_ids:
                    BlogTagRelation(tag_id=tag_new_id, blog_info_id=blog_id).save()

            return HttpResponseRedirect("/blog_detail/%s" % blog_id)
    else:
        if 'blog_id' not in request.GET:
            raise Http404("需要博客id!")
        blog_id = request.GET['blog_id']
        tags = Tag.objects.filter(deleted=False).filter(blogtagrelation__blog_info_id=blog_id)
        tag_ids = [x.id for x in tags]
        form = AddBlogTagForm(initial={"tags": tag_ids, "blog_id": blog_id})
    return render(request, 'myblog/add_blog_tag.html', {'form': form})


@permission_required(["myblog.blog_info.add", "myblog.blog_info.update"], login_url="/user/login")
def blog_edit(request):
    if request.method == 'POST':
        form = EditBlogForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST['blog_id']:
                blog_info = get_object_or_404(BlogInfo, pk=request.POST['blog_id'])
            else:
                blog_info = BlogInfo()
            blog_info.title = request.POST['title']
            blog_info.abstract = request.POST['abstract']
            # if 'cover_img' in request.FILES:
            #     img_fd = request.FILES['cover_img']
            #     img_name = md5(img_fd)
            #     save_file(img_fd, os.path.join(BLOG_COVER_PATH, img_name))
            #     blog_info.cover_img = img_name

            blog_file_path = os.path.join(BLOG_FILE_PATH, request.POST['file_name'])
            write_file(blog_file_path, request.POST['content'])
            blog_info.file_path = request.POST['file_name']
            blog_info.save()
            return HttpResponseRedirect("/blog_detail/%d" % blog_info.id)
    else:
        form = EditBlogForm()

        if 'blog_id' in request.GET:
            blog_info = get_object_or_404(BlogInfo, pk=request.GET['blog_id'])
            blog_file_path = os.path.join(BLOG_FILE_PATH, blog_info.file_path)
            blog_content = read_file_to_string(blog_file_path)
            form.initial = {"blog_id": blog_info.id,
                            "file_name": blog_info.file_path,
                            "title": blog_info.title,
                            "abstract": blog_info.abstract,
                            "content": blog_content
                            }
            form.readonly_field(['blog_id', 'file_name'])

    return render(request, 'myblog/blog_edit.html', {"form": form})


