from django.test import TestCase
from oauthtesting.models import Account

# Create your tests here.


class ExampleTestCase(TestCase):
  def setUp(self):
    Account.objects.create(username = "test", points = 0, bio = "Hi, I'm a dummy account", picture = None)

  def test_account(self):
    account = Account.objects.get(username = "test")
    self.assertEqual(account.points, 0)
