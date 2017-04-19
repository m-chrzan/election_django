from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256)

    class Meta:
        unique_together = ('first_name', 'last_name')

class District(models.Model):
    number = models.IntegerField(unique = True)

class Gmina(models.Model):
    code = models.IntegerField(unique = True)
    name = models.CharField(max_length = 256)

class Circuit(models.Model):
    number = models.IntegerField()
    district = models.ForeignKey("District")
    gmina = models.ForeignKey("Gmina")

class Votes(models.Model):
    candidate = models.ForeignKey("Candidate")
    circuit = models.ForeignKey("Circuit")
    number = models.IntegerField()

    class Meta:
        unique_together = ('candidate', 'circuit')
