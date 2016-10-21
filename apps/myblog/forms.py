from django import forms


class UploadBlogForm(forms.Form):

    file = forms.FileField(label="博客文件")
    file_name = forms.CharField(max_length=5, label="文件名")
    title = forms.CharField(max_length=255, label="标题")
    cover_img = forms.FileField(required=False, label="封面图")
