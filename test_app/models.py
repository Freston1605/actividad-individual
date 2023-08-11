from django.db import models
from .rut_field import RutField

# Define las opciones de categorías como una lista de elecciones (choices)
CATEGORIA_CHOICES = [
    ("lluvia", "Protección contra aguas lluvias"),
    ("ventilacion", "Ventilación"),
    ("accesorios", "Accesorios de instalación"),
]

# Define las opciones de cada categoría como atributos de clase
LLUVIA_CHOICES = [
    ("canal", "Canal"),
    ("bajada", "Bajada"),
    ("caballete", "Caballete"),
    ("cubierta_americana", "Cubierta americana"),
    ("cubierta_acanalada", "Cubierta acanalada"),
    ("cubierta_pizarreño", "Cubierta pizarreño"),
    ("cubierta_otra", "Cubierta otra"),
    ("otros", "Otros"),
]

VENTILACION_CHOICES = [
    ("gorro_chino", "Gorro chino"),
    ("gorro_cometa", "Gorro cometa"),
    ("gorro_eolico", "Gorro eólico"),
    ("tubo", "Tubo"),
    ("ducto", "Ducto"),
    ("anillo", "Anillo"),
    ("conector_t", "Conector T"),
    ("campana", "Campana"),
    ("otros", "Otros"),
]

ACCESORIO_CHOICES = [
    ("abrazadera", "Abrazadera"),
    ("gancho", "Gancho"),
    ("boquilla", "Boquilla"),
    ("cubeta", "Cubeta"),
    ("remache", "Remache"),
    ("silicona", "Silicona"),
    ("reduccion", "Reducción"),
    ("otros", "Otros"),
]


class Material(models.Model):
    """Clase para los materiales de las planchas de las que están los productos."""

    composicion = models.CharField(
        ("Elementos de los que está hecha la plancha"), max_length=50
    )
    espesor = models.IntegerField(("Espesor de la plancha"))
    prepintado = models.BooleanField(("Plancha prepintada o sin pintar"))
    color = models.CharField(
        ("Color de la plancha prepintada"), max_length=50, null=True, blank=True
    )


class Trabajador(models.Model):
    """Clase para los trabajadores de la hojalatería"""

    user = models.ForeignKey(
        "app.Model",
        verbose_name=("Usuario asociado al trabajador"),
        on_delete=models.CASCADE,
    )
    sucursal = models.ForeignKey(
        "app.Model",
        verbose_name=("Sucursal en la que el trabajador se desempeña"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    rut = RutField()
    direccion = models.CharField(
        ("Dirección del trabajador"), max_length=200, null=True, blank=True
    )
    telefono = models.CharField(
        ("Teléfono de contacto del trabajador"), null=True, blank=True
    )


class Sucursal(models.Model):
    """Modelo para las sucursales del negocio"""

    direccion = models.CharField(("Dirección de la sucursal"), max_length=50)
    telefono = models.PhoneNumberField(
        ("Número de teléfono de la sucursal"), null=True, blank=True
    )
    trabajadores = models.ManyToManyField(
        "app.Model",
        verbose_name=("Trabajadores asociados a la sucursal"),
        null=True,
        blank=True,
    )


class Sobrante(models.Model):
    """Modelo para el material sobrante a ser reutilizado"""

    material = models.ForeignKey(
        Material,
        verbose_name=("Material del que está hecho la plancha"),
        on_delete=models.PROTECT,
    )
    existencias = models.IntegerField(("Número en inventario"))
    sucursal = models.ForeignKey(Sucursal, verbose_name=("Modelo de la sucursal en la que está el objeto"), on_delete=models.CASCADE)
    largo = models.DecimalField(max_digits=5, decimal_places=2)
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    alto = models.DecimalField(max_digits=5, decimal_places=2)


class ProductoHojalateria(models.Model):
    """Clase para todos los productos de hojalatería"""

    existencias = models.IntegerField(("Número disponible en inventario"))
    material = models.ForeignKey(
        ("Material del que está hecho el producto"),
        Material,
        on_delete=models.PROTECT,
    )
    trabajador = models.ForeignKey(
        ("Trabajador que fabricó el producto"), Trabajador, on_delete=models.CASCADE
    )
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alto = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    radio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    categoria = models.CharField(
        ("Categoría de producto según uso"), max_length=20, choices=CATEGORIA_CHOICES
    )
    nombre = models.CharField(("Tipo de producto"), max_length=100, choices=[])

    # Define las opciones de cada categoría como atributos de clase
    LLUVIA_CHOICES = [
        ("canal", "Canal"),
        ("bajada", "Bajada"),
        ("caballete", "Caballete"),
        ("cubierta_americana", "Cubierta americana"),
        ("cubierta_acanalada", "Cubierta acanalada"),
        ("cubierta_pizarreño", "Cubierta pizarreño"),
        ("cubierta_otra", "Cubierta otra"),
        ("otros", "Otros"),
    ]

    VENTILACION_CHOICES = [
        ("gorro_chino", "Gorro chino"),
        ("gorro_cometa", "Gorro cometa"),
        ("gorro_eolico", "Gorro eólico"),
        ("tubo", "Tubo"),
        ("ducto", "Ducto"),
        ("anillo", "Anillo"),
        ("conector_t", "Conector T"),
        ("campana", "Campana"),
        ("otros", "Otros"),
    ]

    ACCESORIO_CHOICES = [
        ("abrazadera", "Abrazadera"),
        ("gancho", "Gancho"),
        ("boquilla", "Boquilla"),
        ("cubeta", "Cubeta"),
        ("remache", "Remache"),
        ("silicona", "Silicona"),
        ("reduccion", "Reducción"),
        ("otros", "Otros"),
    ]


    def get_nombre_choices(self):
        # Obtener las opciones según la categoría seleccionada
        categoria_choices = {
            "lluvia": self.LLUVIA_CHOICES,
            "ventilacion": self.VENTILACION_CHOICES,
            "accesorios": self.ACCESORIO_CHOICES,
        }.get(self.categoria, [])

        # Devolver las opciones como una lista de tuplas en el formato requerido por el campo "nombre"
        return [(opcion, opcion) for opcion in categoria_choices]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Actualiza las opciones según la categoría seleccionada
        if self.categoria == "lluvia":
            self._meta.get_field("nombre").choices = LLUVIA_CHOICES
        elif self.categoria == "ventilacion":
            self._meta.get_field("nombre").choices = VENTILACION_CHOICES
        elif self.categoria == "accesorios":
            self._meta.get_field("nombre").choices = ACCESORIO_CHOICES
