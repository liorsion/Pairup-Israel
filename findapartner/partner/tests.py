from django.test import TestCase

from tasks import checkoverduepartner
class PartnerTaskTest(TestCase):
    def test_empty_dbn(self):
        checkoverduepartner().run()
