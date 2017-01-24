from apps.myblog.models import BlogInfo
from apps.myblog.settings import BLOG_CLICK_PREFIX
from django_redis import get_redis_connection
import logging
import traceback

logger = logging.getLogger(__name__)


def sync_blog_click_count():
    try:
        redis_client = get_redis_connection()
        keys = redis_client.scan_iter("%s%s" % (BLOG_CLICK_PREFIX, '*'))
        for key in keys:
            blog_id = key[len(BLOG_CLICK_PREFIX)-1:]
            logger.info("sync blog: %s", blog_id)
            count = redis_client.getset("%s%s" % (BLOG_CLICK_PREFIX, blog_id))
            blogInfo = BlogInfo.objects.filter(blog_id=blog_id)
            blogInfo.click_count += count
            blogInfo.save()
    except:
        logger.error(traceback.format_exc())

