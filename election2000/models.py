from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256)

    class Meta:
        unique_together = ('first_name', 'last_name')

class Voivodeship(models.Model):
    name = models.CharField(max_length = 256, unique = True)

class District(models.Model):
    number = models.IntegerField(unique = True)
    voivodeship = models.ForeignKey("Voivodeship")

class Gmina(models.Model):
    code = models.IntegerField(unique = True)
    name = models.CharField(max_length = 256)

class Circuit(models.Model):
    number = models.IntegerField()
    district = models.ForeignKey("District")
    gmina = models.ForeignKey("Gmina")

    eligible = models.IntegerField(default = 0)
    ballots_given_out = models.IntegerField(default = 0)
    ballots_cast = models.IntegerField(default = 0)
    ballots_invalid = models.IntegerField(default = 0)
    ballots_valid = models.IntegerField(default = 0)

    document = models.FileField(upload_to = 'documents', default = None,
            null = True)

    class Meta:
        unique_together = ('number', 'district', 'gmina')

class Votes(models.Model):
    candidate = models.ForeignKey("Candidate")
    circuit = models.ForeignKey("Circuit")
    number = models.IntegerField()

    class Meta:
        unique_together = ('candidate', 'circuit')
