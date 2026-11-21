from django import forms

from users.models import User, Profile


class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = ("image",)

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"form": "form-control"}),
        required=False,
    )

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