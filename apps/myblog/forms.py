from django import forms
from django.forms import CheckboxSelectMultiple

from ..tag_manage.models import Tag


class UploadBlogForm(forms.Form):

    title = forms.CharField(max_length=255, label="标题")
    abstract = forms.CharField(max_length=500, label="简介")
    file = forms.FileField(label="博客文件")
    file_name = forms.CharField(max_length=255, label="文件名")
    cover_img = forms.FileField(required=False, label="封面图")


class AddBlogTagForm(forms.Form):
    blog_id = forms.IntegerField(label="文章id")
    tags = forms.MultipleChoiceField(label="标签", widget=CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        all_tags = Tag.objects.filter(deleted=False).order_by("priority")
        tag_choices = [(tag.id, tag.tag_name) for tag in all_tags]
        self.fields['tags'].choices = tag_choices


