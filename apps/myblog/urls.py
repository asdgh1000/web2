from django.conf.urls import url

from . import views

app_name = "myblog"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_blog$', views.upload_blog, name='upload_blog'),
    url(r'^blog_detail/(?P<blog_info_id>[0-9]+)$', views.blog_detail, name="blog_detail"),
    url(r'^blog_list', views.blog_list, name='blog_list'),
    url(r'^edit_blog', views.blog_edit, name='edit_blog')
]
