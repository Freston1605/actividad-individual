import re
from django.core.exceptions import ValidationError
from django.db import models


class RutValidator:
    """Esta clase es un validador personalizado que se utiliza para verificar si un valor de RUT dado es válido."""

    def __call__(self, value):
        """Se llama cuando se invoca el validador en un valor de RUT.

        Comprueba si el valor de RUT es válido utilizando el método is_valid_rut.
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
        if value and not self.is_valid_rut(value):
            raise ValidationError("RUT inválido")

    @staticmethod
    def is_valid_rut(rut):
        """Valida si un número de RUT es válido según un patrón específico.

        Esta función toma un número de RUT en formato "12345678-9" y verifica
        si cumple con el patrón numérico y alfanumérico establecido.

        Args:
            rut (str): El número de RUT a validar en formato "12345678-9".

        Returns:
            bool: True si el RUT es válido, False si no lo es.

        Example:
            >>> is_valid_rut("12345678-9")
            True
            >>> is_valid_rut("98765432-K")
            True
            >>> is_valid_rut("12345678-5")
            False
        """
        rut_pattern = r"^\d{7,8}-[0-9kK]$"
        return bool(re.match(rut_pattern, rut))


class RutField(models.CharField):

    """Esta clase RutField es una subclase de models.CharField, que es un campo de texto en un modelo de Django.
    La clase personaliza el comportamiento del campo de texto para que pueda manejar los RUT de manera específica.

    Atributos de clase:
        default_validators = [RutValidator()]: Aquí se establece que el validador personalizado RutValidator se utilizará por defecto para validar los valores ingresados en este campo.
        description = "RUT (Rol Único Tributario)": Se proporciona una descripción para el campo.
    """

    default_validators = [RutValidator()]
    description = "RUT (Rol Único Tributario)"

    def __init__(self, *args, **kwargs):
        """El constructor inicializa el campo con una longitud máxima de 12 caracteres."""
        kwargs["max_length"] = 12
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Convierte y normaliza un valor de RUT recuperado de la base de datos.

        Este método se utiliza para transformar un valor de RUT recuperado de la base de datos
        en una forma normalizada que puede ser manipulada y utilizada en el código.

        Args:
            value (str): El valor de RUT recuperado de la base de datos.

        Returns:
            str: El valor de RUT convertido y normalizado.

        Example:
            >>> field = RutField()
            >>> field.to_python("12.345.678-9")
            '123456789'
            >>> field.to_python("98765432-K")
            '98765432K'
            >>> field.to_python(None)
            None
        """
        if value is None:
            return value
        return value.replace(".", "").replace("-", "").strip().upper()

    def from_db_value(self, value, expression, connection):
        """Convierte un valor de RUT desde la base de datos en una forma utilizable.

        Este método se utiliza para transformar un valor de RUT que ha sido recuperado de la base de datos
        en una forma que pueda ser utilizada y manipulada en el código de la aplicación.

        Args:
            value (str): El valor de RUT recuperado de la base de datos.
            expression: (_type_): _description_ (Descripción del objeto de expresión, si aplica).
            connection (_type_): _description_ (Descripción del objeto de conexión, si aplica).

        Returns:
            _type_: El valor de RUT convertido y listo para su uso.

        Example:
            >>> field = RutField()
            >>> field.from_db_value("12.345.678-9", None, None)
            '123456789'
            >>> field.from_db_value("98765432-K", None, None)
            '98765432K'
        """
        return self.to_python(value)

    def get_prep_value(self, value):
        """Prepara y normaliza un valor de RUT para ser almacenado en la base de datos.

        Este método se utiliza para convertir y normalizar un valor de RUT antes de almacenarlo
        en la base de datos. Realiza la misma conversión que el método to_python.

        Args:
            value (str): El valor de RUT a ser preparado para almacenamiento.

        Returns:
            str: El valor de RUT convertido y normalizado, listo para ser almacenado.

        Example:
            >>> field = RutField()
            >>> field.get_prep_value("12.345.678-9")
            '123456789'
            >>> field.get_prep_value("98765432-K")
            '98765432K'
        """
        return self.to_python(value)

    def formfield(self, **kwargs):
        """Devuelve un objeto de campo de formulario para el campo RUT.

        Este método se utiliza para generar un objeto de campo de formulario que se puede
        utilizar en los formularios de Django para manejar el campo RUT. Se pueden proporcionar
        argumentos adicionales para personalizar el objeto de campo.

        Args:
            **kwargs: Argumentos opcionales para personalizar el objeto de campo.

        Returns:
            RutFormField: Un objeto de campo de formulario para el campo RUT.

        Example:
            >>> field = RutField()
            >>> form_field = field.formfield()
            >>> form_field.label
            'RUT (Rol Único Tributario)'
        """
        defaults = {"form_class": RutFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
