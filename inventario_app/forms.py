from django import forms
from django.contrib.auth.password_validation import validate_password


class RegistrationForm(forms.Form):
    """
    Clase para el formulario de registro de nuevos usuarios.
    Tiene los atributos: nombre de usuario (username),
    nombres (first_name), apellidos (last_name)
    correo electrónico (email), contraseña (password)
    y confirmar la contraseña (confirm_password).
    Cuenta con un método para hacer la verificación del formulario en clean().
    """

    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput, validators=[validate_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Método para realizar la validación del registro del usuario.
        """
        cleaned_data = super().clean()

        return cleaned_data
