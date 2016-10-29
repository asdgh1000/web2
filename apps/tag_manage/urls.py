from django.conf.urls import url

from . import views

app_name = "tag_manage"
urlpatterns = [
    url(r'^$', views.tag_list, name='tag_list'),
    url(r'^add_tag$', views.add_list, name='add_tag')
]
