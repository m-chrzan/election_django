from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from election2000.models import (Candidate, District, Gmina, Circuit, Votes,
        Voivodeship)

class CandidateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Candidate.objects.create(first_name = "Janusz", last_name =
                "Korwin-Mikke")
        Candidate.objects.create(first_name = "Aleksander", last_name =
                "Kwaśniewski")

    def test_query_by_first_name(self):
        korwin = Candidate.objects.get(first_name = "Janusz")
        self.assertEqual(korwin.last_name, "Korwin-Mikke")

    def test_query_by_last_name(self):
        kwaśniewski = Candidate.objects.get(last_name = "Kwaśniewski")
        self.assertEqual(kwaśniewski.first_name, "Aleksander")

    def test_first_name_not_null(self):
        candidate = Candidate(first_name = None, last_name = "Kowalski")
        with self.assertRaises(IntegrityError):
            candidate.save()

    def test_last_name_not_null(self):
        candidate = Candidate(first_name = "Franciszek", last_name = None)
        with self.assertRaises(IntegrityError):
            candidate.save()

    def test_full_name_unique(self):
        candidate = Candidate(first_name = "Janusz", last_name = "Korwin-Mikke")
        with self.assertRaises(IntegrityError):
            candidate.save()

class DistrictTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        voivodeship = Voivodeship.objects.create(name = "V")

        District.objects.create(number = 1, voivodeship = voivodeship)
        District.objects.create(number = 2, voivodeship = voivodeship)
        District.objects.create(number = 3, voivodeship = voivodeship)
        District.objects.create(number = 4, voivodeship = voivodeship)

    def test_query_by_range(self):
        districts = District.objects.filter(number__gte = 2).filter(
                number__lte = 3)
        self.assertEqual(len(districts), 2)

    def test_number_unique(self):
        voivodeship = Voivodeship.objects.get(name = "V")
        district = District(number = 4, voivodeship = voivodeship)
        with self.assertRaises(IntegrityError):
            district.save()

class GminaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Gmina.objects.create(code = 1, name = "Gmina 1")
        Gmina.objects.create(code = 2, name = "Gmina 2")

    def test_query_by_code(self):
        gmina = Gmina.objects.get(code = 1)
        self.assertEqual(gmina.name, "Gmina 1")

    def test_querty_by_name(self):
        gmina = Gmina.objects.get(name = "Gmina 2")
        self.assertEqual(gmina.code, 2)

    def test_code_is_unique(self):
        gmina = Gmina(code = 1, name = "Gmina 3")
        with self.assertRaises(IntegrityError):
            gmina.save()

    def test_name_can_repeat(self):
        Gmina.objects.create(code = 3, name = "Gmina 1")

class CircuitTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        voivodeship = Voivodeship.objects.create(name = "V")

        district1 = District.objects.create(number = 1,
                voivodeship = voivodeship)
        district2 = District.objects.create(number = 2,
                voivodeship = voivodeship)
        district3 = District.objects.create(number = 3,
                voivodeship = voivodeship)

        gmina1 = Gmina.objects.create(code = 1, name = "Gmina 1")
        gmina2 = Gmina.objects.create(code = 2, name = "Gmina 2")
        gmina3 = Gmina.objects.create(code = 3, name = "Gmina 3")
        gmina4 = Gmina.objects.create(code = 4, name = "Gmina 4")

        Circuit.objects.create(number = 1, district = district1, gmina = gmina1)
        Circuit.objects.create(number = 2, district = district1, gmina = gmina1)
        Circuit.objects.create(number = 1, district = district2, gmina = gmina2)
        Circuit.objects.create(number = 2, district = district2, gmina = gmina2)
        Circuit.objects.create(number = 1, district = district2, gmina = gmina3)
        Circuit.objects.create(number = 1, district = district2, gmina = gmina4)
        Circuit.objects.create(number = 2, district = district3, gmina = gmina4)

    def test_query_from_district1(self):
        district = District.objects.get(number = 1)
        circuits = district.circuit_set.all()
        self.assertEqual(len(circuits), 2)

    def test_query_from_district2(self):
        district = District.objects.get(number = 2)
        circuits = district.circuit_set.all()
        self.assertEqual(len(circuits), 4)

    def test_query_from_district3(self):
        district = District.objects.get(number = 3)
        circuits = district.circuit_set.all()
        self.assertEqual(len(circuits), 1)

    def test_no_repeats(self):
        district = District.objects.get(number = 2)
        gmina = Gmina.objects.get(code = 3)
        circuit = Circuit(number = 1, district = district, gmina = gmina)

        with self.assertRaises(IntegrityError):
            circuit.save()

class VotesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        voivodeship = Voivodeship.objects.create(name = "V")

        district = District.objects.create(number = 1,
                voivodeship = voivodeship)
        gmina = Gmina.objects.create(code = 1, name = "Gmina 1")

        circtuit1 = Circuit.objects.create(number = 1, district = district,
                gmina = gmina)
        circtuit2 = Circuit.objects.create(number = 2, district = district,
                gmina = gmina)

        candidate1 = Candidate.objects.create(first_name = "Janusz",
                last_name = "Korwin-Mikke")
        candidate2 = Candidate.objects.create(first_name = "Aleksander",
                last_name = "Kwaśniewski")

        Votes.objects.create(candidate = candidate1, circuit = circtuit1,
                number = 5)
        Votes.objects.create(candidate = candidate1, circuit = circtuit2,
                number = 20)
        Votes.objects.create(candidate = candidate2, circuit = circtuit1,
                number = 10)
        Votes.objects.create(candidate = candidate2, circuit = circtuit2,
                number = 16)

    def test_query_from_candidate(self):
        candidate = Candidate.objects.get(first_name = "Janusz")
        total_votes = sum([votes.number for votes in candidate.votes_set.all()])
        self.assertEqual(total_votes, 25)

    def test_query_from_circuit(self):
        circuit = Circuit.objects.get(number = 1)
        total_votes = sum([votes.number for votes in circuit.votes_set.all()])
        self.assertEqual(total_votes, 15)

    def test_no_repeats(self):
        candidate = Candidate.objects.get(first_name = "Aleksander")
        circuit = Circuit.objects.get(number = 2)
        votes = Votes(candidate = candidate, circuit = circuit,
                number = 11)

        with self.assertRaises(IntegrityError):
            votes.save()

class TestViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username = "user", password = "password")
        voivodeship = Voivodeship.objects.create(name = "V")

        district = District.objects.create(number = 1,
                voivodeship = voivodeship)
        gmina = Gmina.objects.create(code = 1, name = "Gmina 1")

        circtuit1 = Circuit.objects.create(number = 1, district = district,
                gmina = gmina, eligible = 50, ballots_valid = 15, document = None)
        circtuit2 = Circuit.objects.create(number = 2, district = district,
                gmina = gmina, eligible = 60, ballots_valid = 36, document = None)

        candidate1 = Candidate.objects.create(first_name = "Janusz",
                last_name = "Korwin-Mikke")
        candidate2 = Candidate.objects.create(first_name = "Aleksander",
                last_name = "Kwaśniewski")

        Votes.objects.create(candidate = candidate1, circuit = circtuit1,
                number = 5)
        Votes.objects.create(candidate = candidate1, circuit = circtuit2,
                number = 20)
        Votes.objects.create(candidate = candidate2, circuit = circtuit1,
                number = 10)
        Votes.objects.create(candidate = candidate2, circuit = circtuit2,
                number = 16)

    def test_country_view_loads(self):
        response = self.client.get('/Polska/')
        self.assertEqual(response.status_code, 200)

    def test_voivodeship_view_loads(self):
        response = self.client.get('/Polska/V/')
        self.assertEqual(response.status_code, 200)

    def test_district_view_loads(self):
        response = self.client.get('/Polska/V/1/')
        self.assertEqual(response.status_code, 200)

    def test_gmina_view_loads(self):
        response = self.client.get('/Polska/V/1/Gmina 1/')
        self.assertEqual(response.status_code, 200)

    def test_upload_view_denies_not_logged_in(self):
        response = self.client.get('/Polska/V/1/Gmina 1/1/upload/')
        self.assertRedirects(response, '/login/?next=/Polska/V/1/Gmina%25201/1/upload/')

    def test_circuit_view_denies_not_logged_in(self):
        response = self.client.get('/Polska/V/1/Gmina 1/1/')
        self.assertRedirects(response, '/login/?next=/Polska/V/1/Gmina%25201/1/')

    def test_circuit_loads(self):
        self.client.login(username = 'user', password = 'password')
        response = self.client.get('/Polska/V/1/Gmina 1/1/')
        self.assertEqual(response.status_code, 200)
