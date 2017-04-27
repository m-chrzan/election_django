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

class VoivodeshipRegion(Region):
    def __init__(self, name):
        super().__init__(name)

        self.voivodeship = Voivodeship.objects.get(name = name)
        self.locative = "województwie"
        self.subregion_nominative = "okręg"
        self.subregions = self.get_subregions()
        self.template = 'base.html'
        self.votes = self.get_votes()
        self.statistics = self.get_statistics()
        self.region_path = ['Polska', name]

    def get_circuits(self):
        return Circuit.objects.filter(district__voivodeship = self.voivodeship)

    def get_districts(self):
        return District.objects.filter(voivodeship = self.voivodeship)

    def get_subregions(self):
        subregions = []
        for district in self.get_districts():
            statistics = Circuit.objects.filter(district = district).aggregate(Sum('eligible'),
                    Sum('ballots_given_out'))
            subregions.append({
                    'name': str(district.number),
                    'turnout': statistics['ballots_given_out__sum'] /
                        statistics['eligible__sum']
            })

        return subregions

    def get_vote_set(self):
        return Votes.objects.filter(circuit__district__voivodeship =
                self.voivodeship)

class DistrictRegion(Region):
    def __init__(self, name):
        super().__init__(name)

        self.district = District.objects.get(number = int(name))
        self.locative = "okręgu"
        self.subregion_nominative = "gmina"
        self.subregions = self.get_subregions()
        self.template = 'base.html'
        self.votes = self.get_votes()
        self.statistics = self.get_statistics()
        self.region_path = ['Polska', self.district.voivodeship.name, name]

    def get_vote_set(self):
        return Votes.objects.filter(circuit__district = self.district)

    def get_circuits(self):
        return Circuit.objects.filter(district = self.district)

    def get_gminas(self):
        return Gmina.objects.filter(circuit__district =
                self.district).distinct()

    def get_subregions(self):
        subregions = []
        for gmina in self.get_gminas():
            statistics = Circuit.objects.filter(district = self.district,
                    gmina = gmina).aggregate(Sum('eligible'),
                    Sum('ballots_given_out'))
            subregions.append({
                    'name': gmina.name,
                    'turnout': statistics['ballots_given_out__sum'] /
                        statistics['eligible__sum']
            })

        return subregions

class GminaRegion(Region):
    def __init__(self, name, district):
        super().__init__(name)

        self.district = District.objects.get(number = int(district))
        self.locative = "gminie"
        self.subregion_nominative = "obwód"
        self.subregions = self.get_subregions()
        self.template = 'base.html'
        self.votes = self.get_votes()
        self.statistics = self.get_statistics()
        self.region_path = ['Polska', self.district.voivodeship.name,
                str(self.district.number), name]

    def get_circuits(self):
        return Circuit.objects.filter(district = self.district,
                gmina__name = self.name)

    def get_vote_set(self):
        return Votes.objects.filter(circuit__district = self.district,
                    circuit__gmina__name = self.name)

    def get_subregions(self):
        subregions = []
        for circuit in self.get_circuits():
            subregions.append({
                    'name': str(circuit.number),
                    'turnout': circuit.ballots_valid / circuit.eligible,
                    'document': circuit.document
            })

        return subregions
