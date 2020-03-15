from django.test import TestCase
from subscribers.models import Subscriber
from subscribers.tasks import clear_holds


class SubscriberTestCase(TestCase):
    def setUp(self):
        self.users = []
        self.users.append(Subscriber.objects.create(name="Петров Иван Сергеевич",
                                                    uuid="26c940a1-7228-4ea2-a3bce6460b172040",
                                                    balance=1700, status=True, holds=300))

        self.users.append(Subscriber.objects.create(name="Kazitsky Jason",
                                                    uuid="7badc8f8-65bc-449a-8cde855234ac63e1",
                                                    balance=200, status=True, holds=200))

        self.users.append(Subscriber.objects.create(name="Пархоменко Антон Александрович",
                                                    uuid="5597cc3d-c948-48a0-b711-393edf20d9c0",
                                                    balance=10, status=True, holds=300))

        self.users.append(Subscriber.objects.create(name="Петечкин Петр Измаилович",
                                                    uuid="867f0924-a917-4711-939b90b179a96392",
                                                    balance=1000000, status=False, holds=1))

    def test_add(self):
        user = self.users[0]
        old_blanace = user.balance
        addition = 200
        result = user.add(addition)

        self.assertTrue(result)
        self.assertEqual(old_blanace + addition, user.balance)

    def test_add_negative(self):
        user = self.users[0]
        old_balance = user.balance
        addition = -200
        result = user.add(addition)

        self.assertFalse(result)
        self.assertEqual(old_balance, user.balance)

    def test_sub(self):
        user = self.users[0]
        old_holds = user.holds
        old_balance = user.balance
        subtraction = 200
        result = user.subtract(subtraction)

        self.assertTrue(result)
        self.assertEqual(old_balance, user.balance)
        self.assertEqual(old_holds + subtraction, user.holds)

    def test_sub_negative(self):
        user = self.users[0]
        old_holds = user.holds
        old_balance = user.balance
        subtraction = -200
        result = user.subtract(subtraction)

        self.assertFalse(result)
        self.assertEqual(old_balance, user.balance)
        self.assertEqual(old_holds, user.holds)

    def test_impossible_sub(self):
        user = self.users[2]
        old_holds = user.holds
        old_balance = user.balance
        subtraction = user.balance + 1
        result = user.subtract(subtraction)

        self.assertFalse(result)
        self.assertEqual(old_balance, user.balance)
        self.assertEqual(old_holds, user.holds)

    def test_when_status_false(self):
        user = self.users[3]
        money = 200

        self.assertFalse(user.status)
        self.assertFalse(user.add(money))
        self.assertFalse(user.subtract(money))
        self.assertFalse(user.clear_holds())

    def test_clear_holds(self):
        clear_holds()
        for user in Subscriber.objects.all():
            if user.status:
                self.assertEqual(user.holds, 0)
