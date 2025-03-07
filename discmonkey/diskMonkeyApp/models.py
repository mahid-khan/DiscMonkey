from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)

    #maybe consider password hashing

    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class Album(models.Model):
    albumname = models.CharField(max_length=255)

class Review(models.Model):
    albumname = models.CharField(max_length=255)

class Album(models.Model):
    albumname = models.CharField(max_length=255)

class Album(models.Model):
    albumname = models.CharField(max_length=255)

class Album(models.Model):
    albumname = models.CharField(max_length=255)

class Album(models.Model):
    albumname = models.CharField(max_length=255)
