from django.test import TestCase
from django.db import IntegrityError
from election2000.models import Candidate

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
