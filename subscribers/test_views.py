from django.test import TestCase, RequestFactory
from subscribers.models import Subscriber
from subscribers.views import *
import json


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def send_request(self, user, method, json_body):
        request = self.factory.post(f'/{method.__name__}', json_body, content_type='application/json')
        response = method(request)
        json_response = json.loads(response.content.decode())
        user.refresh_from_db()

        return json_response

    def test_ping(self):
        request = self.factory.get('/ping')
        response = ping(request)
        json_response = json.loads(response.content.decode())

        self.assertEqual(json_response['status'], "200 OK")

    def test_status(self):
        user = self.users[3]
        body = json.dumps({"addition": {"uuid": user.uuid}})
        json_response = self.send_request(user, status, body)

        self.assertEqual(json_response['status'], "200 OK")
        self.assertEqual(json_response['addition']['status'], user.status)

    def test_add(self):
        user = self.users[0]
        money = 200
        old_balance = user.balance
        body = json.dumps({"addition": {"uuid": user.uuid,
                                        "money": money}})
        json_response = self.send_request(user, add, body)

        self.assertEqual(json_response['status'], "200 OK")
        self.assertTrue(json_response['result'])
        self.assertEqual(json_response['addition']['balance'], user.balance)
        self.assertEqual(old_balance + money, user.balance)

    def test_sub(self):
        user = self.users[0]
        money = 200
        old_holds = user.holds
        body = json.dumps({"addition": {"uuid": user.uuid,
                                        "money": money}})
        json_response = self.send_request(user, subtract, body)

        self.assertEqual(json_response['status'], "200 OK")
        self.assertTrue(json_response['result'])
        self.assertEqual(json_response['addition']['balance'], user.balance)
        self.assertEqual(old_holds + money, user.holds)
