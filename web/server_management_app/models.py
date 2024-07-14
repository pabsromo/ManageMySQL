from django.db import models

# Create your models here.


class Users(models.Model):
    user_name: models.CharField = models.CharField(max_length=100, unique=True)
    email: models.CharField = models.CharField(max_length=100)


class Images(models.Model):
    image_name: models.CharField = models.CharField(max_length=100, unique=True)
    tag: models.CharField = models.CharField()
    image_hash: models.CharField = models.CharField(max_length=12)


class Containers(models.Model):
    container_name: models.CharField = models.CharField(max_length=100, unique=True)
    container_hash: models.CharField = models.CharField(max_length=12)
    image: models.ForeignKey = models.ForeignKey(Images, on_delete=models.CASCADE)
    created: models.CharField = models.CharField()
    status: models.CharField = models.CharField()
    port: models.IntegerField = models.IntegerField()


class Container_Users(models.Model):
    user: models.ForeignKey = models.ForeignKey(Users, on_delete=models.CASCADE)
    container: models.ForeignKey = models.ForeignKey(
        Containers, on_delete=models.CASCADE
    )


class Databases(models.Model):
    database_name: models.CharField = models.CharField()
    container: models.ForeignKey = models.ForeignKey(
        Containers, on_delete=models.CASCADE
    )
