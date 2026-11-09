from django import forms
from applications.models import SkinRequestModel


class SkinRequestForm(forms.ModelForm):
    class Meta:
        model = SkinRequestModel
        fields = (
            "nickname",
            "message",
        )
