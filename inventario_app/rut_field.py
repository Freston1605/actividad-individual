import re
from typing import Any, Optional, Sequence, Type, Union
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.forms.widgets import Widget


class RutValidator:
    """Esta clase es un validador personalizado que se utiliza para verificar si un valor de RUT dado es válido."""

    def __call__(self, value):
        """Se llama cuando se invoca el validador en un valor de RUT.

        Comprueba que el RUT sea válido al verificar el formato con is_valid_rut y el código verificador con modulo_11.
        Si el RUT no es válido, lanza una excepción de ValidationError.

        Args:
            value (str): El valor de RUT a ser validado.

        Raises:
            ValidationError: Si el RUT no es válido.

        Example:
            >>> validator = RutValidator()
            >>> validator("12345678-9")  # RUT válido
            >>> validator("98765432-K")  # RUT válido
            >>> validator("12345678-5")  # RUT inválido, se lanza una excepción
        """

        if not (self.is_valid_rut(value) and self.modulo_11(value)):
            raise ValidationError("RUT inválido")

    @staticmethod
    def is_valid_rut(rut):
        """Valida si un número de RUT es válido según un patrón específico.

        Esta función toma un número de RUT en formato "12345678-9" y verifica
        si cumple con el patrón numérico y alfanumérico establecido.

        Expresión regular:
            ^: Indica el inicio del string.
            \d{7,8}: Esto coincide con 7 a 8 dígitos consecutivos. El \d es una abreviatura para cualquier dígito del 0 al 9, y {7,8} significa que debe haber entre 7 y 8 repeticiones de \d.
            -: Coincide con un guión literal.
            [0-9kK]: Esto coincide con un dígito del 0 al 9 o la letra 'k' o 'K'.
            $: Indica el final del string.

        Args:
            rut (str): El número de RUT a validar en formato "12345678-9".

        Returns:
            bool: True si el RUT es válido, False si no lo es.
        """
        rut_pattern = r"^\d{7,8}-[0-9kK]$"
        return bool(re.match(rut_pattern, rut))

    @staticmethod
    def modulo_11(rut):
        """Algoritmo para la verificación del dígito verificador del RUT llamado "Módulo 10"

        Args:
            rut (str): RUT completo en formato "12345678-9"

        Returns:
            bool: True si el dígito verificador es correcto y False en el caso contrario
        """

        # Variable que almacena el resultado de la verificación
        digit_check = False

        # Separador de número y dígito verificador (12345678-9 = [12345678, 9])
        lista_rut = rut.split("-", 1)

        # Número del RUT (12345678)
        numero_rut = lista_rut[0]

        # Dígito verificador del RUT (9)
        digito_rut = lista_rut[1]

        # Fáctor inicial de ponderación del cálculo para código de control
        factor = 2

        # Total inicial de la suma del producto del dígito del número del RUT con el factor ponderación
        total = 0

        # Cálculo del total del RUT utilizando el método del módulo 10
        for digit in reversed(numero_rut):
            total += int(digit) * factor
            factor = (factor + 1) % 8 or 2

        # Cálculo del módulo del RUT
        divisor = 11
        modulo_rut = total % divisor

        # Verificación del dígito ingresado
        verificaciones = {
            "0": 11,
            "1": 0,
            "2": 9,
            "3": 8,
            "4": 7,
            "5": 6,
            "6": 5,
            "7": 4,
            "8": 3,
            "9": 2,
            "k": 10,
        }

        # Prueba lógica del dígito verificador
        if verificaciones.get(digito_rut.lower()) == modulo_rut:
            digit_check = True
        return digit_check


from django import forms

class RutField(forms.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes personalizar la inicialización del campo

    def clean(self, value):
        # Aquí puedes realizar la validación y limpieza del valor del RUT
        # Si es válido, puedes devolver el valor limpio, de lo contrario, levanta una ValidationError