import uuid
from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=150)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    balance = models.IntegerField()
    holds = models.IntegerField()
    status = models.BooleanField()

    def add(self, addition):
        if not self.status or addition < 0:
            return False
        self.balance += addition
        self.save()
        return True

    def subtract(self, subtraction):
        if not self.status or subtraction < 0 or self.balance - self.holds - subtraction < 0:
            return False
        self.holds += subtraction
        self.save()
        return True

    def clear_holds(self):
        if not self.status:
            return False
        self.balance -= self.holds
        self.holds = 0
        self.save()
        return True

    def __str__(self):
        return self.name
