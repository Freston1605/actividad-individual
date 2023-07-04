from django import forms

class InputForm(forms.Form):
    """Formulario para registrar nuevos usuarios. Pide nombre (first_name), apellido (last_name) y contraseña."""
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput())