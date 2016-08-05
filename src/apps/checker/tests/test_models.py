from django.test import TestCase

from checker.models import Query
import checker.tests.factories as factories


class ModelsTestCase(TestCase):

    def tearDown(self):
        Query.objects.all().delete()

    def test_get_latest_status(self):
        factories.QueryFactory(status=True)
        factories.QueryFactory(status=None)
        factories.QueryFactory(status=False)

        self.assertFalse(Query.get_latest_status())

    def test_get_unhandled_queries(self):
        data = [dict(a=1, b=2)]
        query_1 = factories.QueryFactory(status=None, data=data)
        factories.QueryFactory(status=True, data=data)

        self.assertEqual(len(Query.get_unhandled_queries()), 1)

        test_data = [{'data': data, 'id': query_1.id}]
        self.assertListEqual(Query.get_unhandled_queries(), test_data)

    def test_update_statuses(self):
        query_1 = factories.QueryFactory(status=None)
        query_2 = factories.QueryFactory(status=None)
        factories.ResultFactory(query=query_1)
        factories.QueryExceptionFactory(query=query_2)
        factories.QueryExceptionFactory(query=query_2)

        Query.update_statuses()

        self.assertTrue(Query.objects.filter(
            result__isnull=False).first().status)
        self.assertEqual(Query.objects.filter(status=True).count(), 1)
        self.assertEqual(Query.objects.filter(
            status=True).first().id, query_1.id)

        self.assertFalse(Query.objects.filter(
            exceptions__isnull=False).first().status)
        self.assertEqual(Query.objects.filter(
            exceptions__isnull=False).distinct().count(), 1)
