from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import Profile


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )
            login(request, user)

            if user.profile.role == Profile.ROLE_STUDENT:
                return redirect("basket")

            return redirect("tutor_students")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        user = self.request.user

        if hasattr(user, "profile") and user.profile.role == Profile.ROLE_STUDENT:
            return "/academics/basket/"

        return "/"


class CustomLogoutView(LogoutView):
    next_page = "login" 