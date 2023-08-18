from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Trabajador, Material, Sucursal
from django.contrib.auth.models import User

class RegistroMaterialForm(forms.ModelForm):
    """
    Esta clase define un formulario para registrar información sobre el material de hojalata que compone los productos.

    Args:
        forms (module): Clase para la creación de formularios en Django.
    """

    # Opciones para el tipo de composición del material de hojalata.
    COMPOSICION_CHOICES = (
        "Zinc galvanizado",
        "Zinc-aluminio",
        "Zinc prepintado",
        "Laminado en frío",
    )

    # Campo de elección para la composición del material.
    composicion_input = forms.ChoiceField(
        label="Material del que está recubierta la hojalata",
        choices=COMPOSICION_CHOICES,
        required=True,
    )

    # Campo decimal para el espesor de la plancha en centímetros.
    espesor_input = forms.DecimalField(
        label="Espesor de la plancha en centímetros",
        max_digits=1,
        decimal_places=3,
    )

    # Campo booleano para indicar si la plancha tiene o no prepintado.
    prepintado_input = forms.BooleanField(
        label="Plancha con o sin prepintado", required=True
    )

    # Campo de texto para especificar el color de la plancha.
    color_input = forms.CharField(
        label="Color de la plancha",
        max_length=50,
        required=False,
        null=True,
        blank=True,
    )


class RegistroProductoForm(forms.ModelForm):
    """Formulario para el registro de productos de hojalatería

    Args:
        forms (module): Módulo que contiene clases para la creación de formularios en Django.
    """

    # Elecciones: Define las opciones de categorías como una lista de elecciones (choices)

    CATEGORIA_CHOICES = (
        (
            "lluvia",
            (
                ("canal", "Canal"),
                ("bajada", "Bajada"),
                ("caballete", "Caballete"),
                (
                    "cubierta",
                    (
                        ("americana", "Cubierta Americana"),
                        ("acanalada", "Cubierta Acanalada"),
                        ("pizarreño", "Cubierta Pizarreño"),
                        ("otra", "Cubierta Otros"),
                    ),
                ),
                ("otros", "Otros"),
            ),
        ),
        (
            "ventilacion",
            (
                (
                    "gorro",
                    (
                        ("chino", "Gorro Chino"),
                        ("cometa", "Gorro Cometa"),
                        ("eolico", "Gorro Eólico"),
                    ),
                ),
                ("tubo", "Tubo"),
                ("ducto", "Ducto"),
                ("anillo", "Anillo"),
                ("conector_t", "Conector T"),
                ("campana", "Campana"),
                ("otros", "Otros"),
            ),
        ),
        (
            "accesorios",
            (
                ("abrazadera", "Abrazadera"),
                ("gancho", "Gancho"),
                ("boquilla", "Boquilla"),
                ("cubeta", "Cubeta"),
                ("remache", "Remache"),
                ("silicona", "Silicona"),
                ("reduccion", "Reducción"),
                ("otros", "Otros"),
            ),
        ),
    )

    # Campo para el tipo de producto
    categoria_input = forms.ChoiceField(
        "Tipo de producto", choices=CATEGORIA_CHOICES, required=True
    )
    # Campo para el tipo de material del producto
    material_input = forms.ModelMultipleChoiceField(
        "Material del que está hecho el producto",
        queryset=Material.objects.all(),
        required=True,
    )
    # Campo para el número en inventario
    existencias_input = forms.IntegerField(
        "Número de productos en inventario", required=False
    )
    # Campo para los trabajadores responsables del producto
    trabajador_input = forms.ModelMultipleChoiceField(
        "Trabajadores que manufacturaron el producto", queryset=Trabajador.objects.all()
    )
    # Campo para las dimensiones del producto si es que aplica
    largo_input = forms.DecimalField(
        "Largo del producto en metros", max_digits=3, decimal_places=3
    )
    ancho_input = forms.DecimalField(
        "Ancho del producto", max_digits=3, decimal_places=3
    )
    alto_input = forms.DecimalField("Alto del producto", max_digits=3, decimal_places=3)
    radio_input = forms.DecimalField(
        "Radio del producto", max_digits=3, decimal_places=3
    )


class RegistroSucursalForm(forms.ModelForm):
    """Formulario de registro para las sucursales de la compañía

    Args:
        forms (module): Clase de Django de la que se hereda la funcionalidad de los formularios
    """

    direccion = forms.CharField(
        "Dirección de la sucursal", max_length=200, required=True
    )
    telefono = forms.CharField(
        "Número de teléfono de la sucursal", max_length=10, required=True
    )
    trabajadores = forms.ModelChoiceField(
        verbose="Trabajadores asociados a la sucursal",
        queryset=Trabajador.objects.all(),
    )


class RegistroSobranteForm(forms.ModelForm):
    """Formulario para registrar el material sobrante o despunte al fabricar productos de hojalatería

    Args:
        forms (module): Clase de Django de la que se hereda la funcionalidad de los formularios
    """

    # Campo para el material que compone el sobrante
    material_input = forms.ModelChoiceField(
        "Material que compone el sobrante",
        queryset=Material.objects.all(),
        required=True,
    )

    # Campo para el número de existencias en inventario
    existencias_input = forms.IntegerField(
        "Número en inventario", min_value=0, required=True
    )

    # Campo para la sucursal que almacena el sobrante
    sucursal_input = forms.ModelChoiceField(
        "Sucursal que almacena el sobrante",
        queryset=Sucursal.objects.all(),
        required=True,
    )

    # Campos para las dimensiones del sobrante en metros
    largo_input = forms.DecimalField(max_digits=3, decimal_places=3, required=True)
    ancho_input = forms.DecimalField(max_digits=3, decimal_places=3, required=True)

class RegistroTrabajador(forms.ModelForm):
    """Formulario para registrar a los trabajadores

    Args:
        forms (module): Clase de Django de la que se hereda la funcionalidad de los formularios
    """
    # Campo para el RUT
    rut_input = forms.