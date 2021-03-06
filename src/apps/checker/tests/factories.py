import random

from django.utils import timezone

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from checker.models import Query, Result, QueryException


class FuzzyJson(fuzzy.BaseFuzzyAttribute):

    def __init__(self, count=5):
        super(FuzzyJson, self).__init__()
        self.count = count

    def fuzz(self):

        data = [
            dict(a=random.randrange(100),
                 b=random.randrange(100))
            for _ in range(1, self.count)]
        return data

    def invalid_fuzz(self):
        invalid_set = [
            dict(a=[]), dict(), dict(a=1, b='foo'), dict(a=1, b='foo')
        ]
        data = [
            dict(a=random.randrange(100),
                 b=random.randrange(100))
            for _ in range(1, self.count)]

        invalid_data = []
        for _ in range(1, self.count):
            for d in invalid_set:
                invalid_data.append(d)

        return data + invalid_data


class QueryFactory(DjangoModelFactory):
    status = None
    data = FuzzyJson()
    date = fuzzy.FuzzyDateTime(timezone.now())

    class Meta:
        model = Query


class ResultFactory(DjangoModelFactory):
    query = factory.SubFactory(QueryFactory)
    result = FuzzyJson()

    class Meta:
        model = Result


class QueryExceptionFactory(DjangoModelFactory):
    query = factory.SubFactory(QueryFactory)
    traceback = fuzzy.FuzzyText()
    date = fuzzy.FuzzyDateTime(timezone.now())

    class Meta:
        model = QueryException
