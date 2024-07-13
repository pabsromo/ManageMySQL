from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)


class Servers(models.Model):
    DBMS_OPTIONS = [
        ("MySQL", "MySQL"),
        ("TBD", "To Be Determined"),
    ]

    name = models.CharField(max_length=100)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    dbms = models.CharField(max_length=100, choices=DBMS_OPTIONS, default="TBD")
