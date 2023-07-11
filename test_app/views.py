from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegistrationForm


def landing_page(request):
    return render(request, "landing.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario si es válido
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Crear un nuevo usuario
            new_user = User.objects.create_user(username=username, password=password)

            # Redirigir a la página de bienvenida después del registro
            return redirect("welcome")
    else:
        form = RegistrationForm()
    return render(request, "registration.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("welcome")


@login_required
def welcome(request):
    return render(request, "welcome.html")


def logout_view(request):
    logout(request)
    return redirect("landing")

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', ({'users': users}))