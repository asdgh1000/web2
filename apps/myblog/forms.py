from django import forms
from django.forms import CheckboxSelectMultiple, Textarea

from ..tag_manage.models import Tag


class UploadBlogForm(forms.Form):

    title = forms.CharField(max_length=255, label="标题")
    abstract = forms.CharField(max_length=500, label="简介", widget=Textarea())
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


class EditBlogForm(forms.Form):
    blog_id = forms.IntegerField(label="文章id", required=False)
    title = forms.CharField(min_length=1, max_length=255, label="标题")
    abstract = forms.CharField(min_length=10, max_length=500, label="简介", widget=Textarea())
    file_name = forms.CharField(min_length=1, max_length=255, label="文件名")
    cover_img = forms.FileField(required=False, label="封面图")
    content = forms.CharField(widget=Textarea(), min_length=10)

    def init_field(self, field_map):
        '''
        初始化对应field，并使其只读
        :return:
        '''
        for key, value in field_map:
            self.fields[key].initial = value
            self.fields[key].widget.attrs['readonly'] = True



