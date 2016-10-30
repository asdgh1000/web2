from django.conf.urls import url

from . import views

app_name = "user_manage"
urlpatterns = [
    url(r'^login$', views.login, name='login'),
]
