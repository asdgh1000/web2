from django import forms


class AddTagForm(forms.Form):

    tag_name = forms.CharField(max_length=20, label="标签名", required=True)
    priority = forms.ChoiceField(label="优先级", choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3")])
