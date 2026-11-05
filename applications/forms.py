from django import forms
from applications.models import SkinRequestModel


class SkinRequestform(forms.ModelForm):
    class Meta:
        model = SkinRequestModel
        field = ['nickname', 'message']
