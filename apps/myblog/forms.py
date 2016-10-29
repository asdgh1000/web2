from django import forms


class UploadBlogForm(forms.Form):

    title = forms.CharField(max_length=255, label="标题")
    abstract = forms.CharField(max_length=500, label="简介")
    file = forms.FileField(label="博客文件")
    file_name = forms.CharField(max_length=255, label="文件名")
    cover_img = forms.FileField(required=False, label="封面图")
