"""
El siguiente guión es para ser ejecutado con la consola shell de django.
Añade 5 usuarios a la aplicación test_app para que puedan ser visualizados y manipulados.
El modelo que se utiliza es CustomUser, que cuenta con los campos: username,
email, password, first_name, last_name y address.
"""

from django.contrib.auth import get_user_model

User = get_user_model()

# Usuario 1
username = "user1"
email = "user1@example.com"
password = "password1"
user1 = User.objects.create_user(username=username, email=email, password=password, first_name="Nombre1", last_name="Apellido1", address="Dirección1")

# Usuario 2
username = "user2"
email = "user2@example.com"
password = "password2"
user2 = User.objects.create_user(username=username, email=email, password=password, first_name="Nombre2", last_name="Apellido2", address="Dirección2")

# Usuario 3
username = "user3"
email = "user3@example.com"
password = "password3"
user3 = User.objects.create_user(username=username, email=email, password=password, first_name="Nombre3", last_name="Apellido3", address="Dirección3")

# Usuario 4
username = "user4"
email = "user4@example.com"
password = "password4"
user4 = User.objects.create_user(username=username, email=email, password=password, first_name="Nombre4", last_name="Apellido4", address="Dirección4")

# Usuario 5
username = "user5"
email = "user5@example.com"
password = "password5"
user5 = User.objects.create_user(username=username, email=email, password=password, first_name="Nombre5", last_name="Apellido5", address="Dirección5")