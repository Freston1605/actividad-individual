from django import forms

class RegistrationForm(forms.Form):
    """
    Clase para el formulario de registro de nuevos usuarios.
    Tiene los atributos: nombre de usuario (username), contraseña (password)
    y confirmar la contraseña (confirm_password).
    Cuenta con un método para hacer la verificación en clean().
    """
    username = forms.CharField(max_length=150)
    # email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Método para realizar la validación del registro del usuario.
        Limpia las contraseñas de la instancia, confirma que estén presentes
        y que sean iguales.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data