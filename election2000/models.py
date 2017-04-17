from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256)

class District(models.Model):
    number = models.IntegerField(unique = True)

class Gmina(models.Model):
    name = models.CharField(max_length = 256)