from django import forms


class UploadBlogForm(forms.Form):

    title = forms.CharField(max_length=255)
    file_name = forms.CharField(max_length=5)
    file = forms.FileField()
    cover_img = forms.FileField(required=False)
