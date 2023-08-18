from django.db import models
from .rut_field import RutField


class Material(models.Model):
    """Clase para los materiales de las planchas de las que están los productos.

    Args:
        models(module): Clase de Django de la que se hereda la funcionalidad de los modelos.

    """

    # Campo para los elementos que componen el material (zinc, aluminio, entre otros)
    composicion = models.CharField(
        ("Elementos de los que está hecha la plancha"), max_length=50
    )
    # Campo para el espesor de la plancha en centímetros
    espesor = models.DecimalField(
        "Espesor de la plancha en centímetros", max_digits=1, decimal_places=3
    )
    # Campo booleano para marcar una plancha como prepintada o no
    prepintado = models.BooleanField(("Plancha prepintada o sin pintar"))
    
    # Campo para asignar un color al prepintado de una plancha
    color = models.CharField(
        ("Color de la plancha prepintada"), max_length=50, null=True, blank=True
    )


class Trabajador(models.Model):
    """Clase para los trabajadores de la hojalatería
    
    Args:
        models(module): Clase de Django de la que se hereda la funcionalidad de los modelos.
    """

    # Campo para asociar un modelo de usuario al trabajador
    user = models.ForeignKey(
        "app.Model",
        verbose_name=("Usuario asociado al trabajador"),
        on_delete=models.CASCADE,
    )
    
    # Campo para asociar un modelo de sucursal al trabajador
    sucursal = models.ForeignKey(
        "app.Model",
        verbose_name=("Sucursal en la que el trabajador se desempeña"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    
    # Campo para registrar el RUT del trabajador
    rut = RutField()
    direccion = models.CharField(
        ("Dirección del trabajador"), max_length=200, null=True, blank=True
    )
    
    # Campo para registrar un número de contacto del trabajador
    telefono = models.CharField(
        ("Teléfono de contacto del trabajador"), null=True, blank=True
    )


class Sucursal(models.Model):
    """Modelo para las sucursales del negocio

    Args:
    models(module): Clase de Django de la que se hereda la funcionalidad de los modelos.

    """

    # Campo para la dirección de la sucursal
    direccion = models.CharField(("Dirección de la sucursal"), max_length=200)

    # Campo para el teléfono de contacto de la sucursal
    telefono = models.CharField(
        ("Número de teléfono de la sucursal"), null=False, blank=False
    )

    # Campo para los trabajadores asociados a la sucursal
    trabajadores = models.ManyToManyField(
        "app.Model",
        verbose_name=("Trabajadores asociados a la sucursal"),
        null=True,
        blank=True,
    )


class Sobrante(models.Model):
    """Modelo para el material sobrante a ser reutilizado

    Args:
        models(module): Clase de Django de la que se hereda la funcionalidad de los modelos.
    """

    # Campo para el modelo del material que compone el sobrante
    material = models.ForeignKey(
        Material,
        verbose_name=("Material del que está hecho la plancha"),
        on_delete=models.PROTECT,
    )
    # campo para el número de existencias en inventario
    existencias = models.IntegerField(("Número en inventario"))
    # Campo para la sucursal que almacena el sobrante
    sucursal = models.ForeignKey(
        Sucursal,
        verbose_name=("Modelo de la sucursal en la que está el objeto"),
        on_delete=models.CASCADE,
    )
    # Camnpos para las dimensiones del sobrante en metros
    largo = models.DecimalField(max_digits=3, decimal_places=2)
    ancho = models.DecimalField(max_digits=3, decimal_places=2)


class ProductoHojalateria(models.Model):
    """Clase para todos los productos de hojalatería

    Args:
        models(module): Clase de Django de la que se hereda la funcionalidad de los modelos.
    """

    # Campo para la categoría del producto en el formulario RegistroProductoForm se detallan las opciones
    categoria = models.CharField("Tipo de producto", max_length=100)

    # Campo para el número en inventario
    existencias = models.IntegerField(("Número disponible en inventario"))

    # Campo para el modelo de los materiales de los que están hechos los productos
    material = models.ManyToManyField(
        Material, verbose_name=("Material del que está hecho el producto")
    )

    # Campo para los modelos de los trabajadores que hicieron el producto
    Trabajador = models.ManyToManyField(
        Trabajador, verbose_name=("Trabajadores que fabricaron el producto")
    )

    # Campo provisorio para las dimensiones del producto en metros
    largo = models.DecimalField(max_digits=3, decimal_places=3, null=True, blank=True)
    ancho = models.DecimalField(max_digits=3, decimal_places=3, null=True, blank=True)
    alto = models.DecimalField(max_digits=3, decimal_places=3, null=True, blank=True)
    radio = models.DecimalField(max_digits=3, decimal_places=3, null=True, blank=True)
