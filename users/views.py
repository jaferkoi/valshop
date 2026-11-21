from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.forms import ProfileForm, SignUpForm

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно изменён!")

            return redirect("users:profile")

        messages.error(request, "Проверьте правильность заполнения формы")

    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, "users/profile.html", {"form": form})


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.save()
        messages.success(request, "Вы успешно зарегестрировались!")
        return redirect("users:login")

    return render(request, "users/signup.html", {"form": form})
