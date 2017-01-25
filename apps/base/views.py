from ..myblog.models import BlogInfo
from ..tag_manage.models import Tag
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response


def render_with_public_item(request, page, data=None):
    newest_bloginfo_list = BlogInfo.objects.order_by("-created")[0:5]
    hotest_bloginfo_list = BlogInfo.objects.order_by("-click_count")[0:5]
    tags = get_list_or_404(Tag.objects.filter(deleted=False))

    if data is None:
        data = {}

    data.update({
        'newest_blog_list': [{"id": blog.id, "title": blog.title} for blog in newest_bloginfo_list],
        'hotest_blog_list': [{"id": blog.id, "title": blog.title} for blog in hotest_bloginfo_list],
        'tag_list': tags
    })

    return render(request, page, data)

