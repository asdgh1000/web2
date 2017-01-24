from django.core.cache import cache
from .models import BlogInfo
from .settings import BLOG_CLICK_PREFIX


def sync_blog_click_count():
    redis_client = cache.get_client()
    keys = redis_client.scan_iter("%s%s" % (BLOG_CLICK_PREFIX, '*'))
    for key in keys:
        blog_id = key[19:]
        count = redis_client.getset("%s%s" % (BLOG_CLICK_PREFIX, blog_id))
        blogInfo = BlogInfo.objects.filter(blog_id=blog_id)
        blogInfo.click_count += count
        blogInfo.save()

