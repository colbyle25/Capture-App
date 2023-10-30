from django.test import TestCase
from oauthtesting.models import Account, Friends, POI, Captured, Message, TextMessage, Like
from datetime import datetime
import datetime as dt

# Create your tests here.


class ExampleTestCase(TestCase):
    def setUp(self):
        user1 = Account.objects.create(username="test", points=0, bio="Hi, I'm a dummy account", picture=None)
        user2 = Account.objects.create(username="test2", points=0, bio="I like bread", picture=None)
        user3 = Account.objects.create(username="test3", points=121121224534, bio="", picture=None)
        user4 = Account.objects.create(username="test4", points=0, bio="Who needs friends?", picture=None)

        Friends.objects.create(user1=user1, user2=user2)
        Friends.objects.create(user1=user3, user2=user1)

        TextMessage.objects.create(username=user1, time=datetime.now(),
                                   longitude=0, latitude=0, text="This is a message")


    def test_account(self):
        account = Account.objects.get(username="test")
        self.assertEqual(account.points, 0)

    def test_not_an_account(self):
        account = Account.objects.filter(username="username")
        self.assertEqual(len(account), 0)

    def test_friend(self):
        user1 = Account.objects.get(username="test")
        user2 = Account.objects.get(username="test2")
        friend = Friends.objects.filter(user1=user1, user2=user2) | Friends.objects.filter(user1=user2, user2=user1)
        self.assertEqual(len(friend), 1)

    def test_multiple_friends(self):
        user1 = Account.objects.get(username="test")
        friend = Friends.objects.filter(user1=user1) | Friends.objects.filter(user2=user1)
        self.assertEqual(len(friend), 2)

    def test_friendless(self):
        user4 = Account.objects.get(username="test4")
        friend = Friends.objects.filter(user1=user4) | Friends.objects.filter(user2=user4)
        self.assertEqual(len(friend), 0)

    def test_text(self):
        user1 = Account.objects.get(username="test")
        text = TextMessage.objects.get(username=user1)
        self.assertEqual(text.text, "This is a message")

    def test_two_text(self):
        user2 = Account.objects.get(username="test2")
        t = datetime.now()
        TextMessage.objects.create(username=user2, time=t,
                                   longitude=0, latitude=0, text="This is another message")
        TextMessage.objects.create(username=user2, time=t - dt.timedelta(seconds=15),
                                   longitude=0, latitude=0, text="This is another another message")
        text = TextMessage.objects.get(username=user2, time=t)
        text2 = TextMessage.objects.get(username=user2, time=(t - dt.timedelta(seconds=15)))

        self.assertEqual(text.text, "This is another message")
        self.assertEqual(text2.text, "This is another another message")

