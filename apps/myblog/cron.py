from .models import BlogInfo
from .settings import BLOG_CLICK_PREFIX
from django_redis import get_redis_connection


def sync_blog_click_count():
    redis_client = get_redis_connection()
    keys = redis_client.scan_iter("%s%s" % (BLOG_CLICK_PREFIX, '*'))
    for key in keys:
        blog_id = key[len(BLOG_CLICK_PREFIX)-1:]
        count = redis_client.getset("%s%s" % (BLOG_CLICK_PREFIX, blog_id))
        blogInfo = BlogInfo.objects.filter(blog_id=blog_id)
        blogInfo.click_count += count
        blogInfo.save()

