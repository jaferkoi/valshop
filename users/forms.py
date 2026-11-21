from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Profile


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ("image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["name"].initial = self.instance.user.name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.name = self.cleaned_data["name"]
        user.save()
        if commit:
            profile.save()
        return profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs.update({"class": "form-control"})

