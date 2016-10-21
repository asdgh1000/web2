from django.conf.urls import url

from . import views

app_name = "myblog"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_blog$', views.upload_blog, name='upload_blog')
]
