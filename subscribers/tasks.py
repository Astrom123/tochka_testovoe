from __future__ import absolute_import, unicode_literals
from celery import task
from subscribers.models import Subscriber
from django.db.models import F


@task()
def clear_holds():
    for subscriber in Subscriber.objects.all():
        subscriber.clear_holds()