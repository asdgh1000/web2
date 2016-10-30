"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # 默认目录
    url(r'^', include('apps.myblog.urls')),
    url(r'^tag/', include('apps.tag_manage.urls')),
    url(r'^user/', include('apps.user_manage.urls')),

    # 管理目录
    url(r'^admin/', admin.site.urls),
    # robots.txt文件
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # 站点地图
    url(r'^sitemap\.txt$', TemplateView.as_view(template_name='sitemap.txt', content_type='text/plain')),
]
