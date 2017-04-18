from django.test import TestCase
from django.db import IntegrityError
from election2000.models import Candidate, District, Gmina, Circuit

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

class DistrictTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        District.objects.create(number = 1)
        District.objects.create(number = 2)
        District.objects.create(number = 3)
        District.objects.create(number = 4)

    def test_query_by_range(self):
        districts = District.objects.filter(number__gte = 2).filter(
                number__lte = 3)
        self.assertEqual(len(districts), 2)

    def test_number_unique(self):
        district = District(number = 4)
        with self.assertRaises(IntegrityError):
            district.save()

class CircuitTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        district1 = District.objects.create(number = 1)
        district2 = District.objects.create(number = 2)
        district3 = District.objects.create(number = 3)

        gmina1 = Gmina.objects.create(name = "Gmina 1")
        gmina2 = Gmina.objects.create(name = "Gmina 2")
        gmina3 = Gmina.objects.create(name = "Gmina 3")
        gmina4 = Gmina.objects.create(name = "Gmina 4")

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
