from django import forms


class UploadBlogForm(forms.Form):

    file = forms.FileField()
    file_name = forms.CharField(max_length=5)
    title = forms.CharField(max_length=255)
    cover_img = forms.FileField(required=False)
