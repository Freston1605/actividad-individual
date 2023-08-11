from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistrationForm


def landing_page(request):
    return render(request, "landing.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario si es válido
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["password"]

            # Verificando las contraseñas
            if password != confirm_password:
                messages.error(request, "Views: Las contraseñas no coinciden.")
            else: 
                # Crear un nuevo usuario
                new_user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )

                # Guardar al usuario en la base de datos
                new_user.save()

                # Iniciando sesión con el nuevo usuario
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)

                    # Redirigir a la página de bienvenida después del registro
                    return redirect("welcome")

        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, "registration.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("welcome")

    def form_invalid(self, form):
        """
        Método para manejar el caso de inicio de sesión inválido.
        Aquí puedes personalizar la forma en que se muestran los errores al usuario.
        """
        messages.error(self.request, "Inicio de sesión inválido. Verifica tus credenciales.")
        return super().form_invalid(form)

@login_required
def welcome(request):
    return render(request, "welcome.html")


def logout_view(request):
    logout(request)
    return redirect("landing")

@login_required
def user_list(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Necesitas iniciar sesión para ver esta página.')
        return redirect('login')
    
    users = User.objects.all()
    return render(request, "user_list.html", ({"users": users}))
