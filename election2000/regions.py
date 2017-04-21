from election2000.models import (Gmina, District, Circuit, Candidate, Votes,
        Voivodeship)
from django.db.models import Sum

class Region:
    def __init__(self, name):
        self.name = name

    def get_votes(self):
        candidates = Candidate.objects.all()
        votes = {}
        vote_set = self.get_vote_set()
        for candidate in candidates:
            votes[candidate.first_name + ' ' + candidate.last_name] = vote_set.filter(
                    candidate = candidate).aggregate(Sum('number'))['number__sum']
        return votes

    def get_statistics(self):
        aggregated = self.get_circuits().aggregate(Sum('ballots_valid'),
                Sum('ballots_given_out'))
        return {
                'ballots_valid': aggregated['ballots_valid__sum'],
                'ballots_given_out': aggregated['ballots_given_out__sum']
                }

class CountryRegion(Region):
    def __init__(self):
        super().__init__("Polska")

        self.locative = "kraju"
        self.subregion_nominative = "województwo"
        self.subregions = self.get_subregions()
        self.template = 'base.html'
        self.votes = self.get_votes()
        self.statistics = self.get_statistics()
        self.region_path = ['Polska']

    def get_circuits(self):
        return Circuit.objects.all()

    def get_subregions(self):
        subregions = []
        for voivodeship in Voivodeship.objects.all():
            statistics = Circuit.objects.filter(district__voivodeship =
                    voivodeship).aggregate(Sum('eligible'),
                    Sum('ballots_given_out'))
            subregions.append({
                    'name': voivodeship.name,
                    'turnout': statistics['ballots_given_out__sum'] /
                        statistics['eligible__sum']
            })

        return subregions

    def get_vote_set(self):
        return Votes.objects.all()
