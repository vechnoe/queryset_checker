import json

from django.test import TestCase

from checker.models import Query, Result, QueryException
from checker.utils import _result, check_func,  handle_queries, handle_results
import factories


class UtilsTestCase(TestCase):
    def setUp(self):
        self.valid_item = dict(a=1, b=2)
        self.invalid_item = dict(a='foo', b=42)
        self.invalid_query = dict(data=[dict(a='foo', b=42)], id=1)

    def test__result_valid_item(self):
        _result(self.valid_item, 1, [])
        self.assertDictEqual(
            _result(self.valid_item, 42, []), dict(result=3))

    def test_check_func_valid_query(self):
        query = dict(data=[dict(a=1, b=2)], id=1)
        result = check_func(query, [])
        self.assertListEqual(result, [dict(result=3)])

    def test_check_func_invalid_query(self):
        self.assertListEqual(check_func(self.invalid_query, []), [None])

    def test_check_func_pass_valid_with_invalid(self):
        valid_with_invalid_data = dict(data=[
            dict(a='foo', b=42), dict(a=1, b=2)
        ], id=1)
        result = check_func(valid_with_invalid_data, [])

        self.assertListEqual(result, [None, dict(result=3)])

    def test_handle_queries_invalid_query_store_exception(self):
        query_obj = factories.QueryFactory(data=[self.invalid_item])
        queries = json.dumps(Query.get_unhandled_queries())

        handle_queries(queries)
        exception = QueryException.objects.first()

        self.assertEqual(QueryException.objects.count(), 1)
        self.assertEqual(exception.query.id, query_obj.id)
        # Exception class in the traceback
        self.assertIn('TypeError', exception.traceback)
        # Exception body in the traceback
        self.assertIn(str(self.invalid_item), exception.traceback)

    def test_handle_queries_set_invalid_data_as_none(self):
        invalid_query = json.dumps(
            [dict(data=[dict(a='foo', b=42)], id=1),
             dict(data=[dict(a=1, b=2)], id=2)]
        )
        result = json.loads(handle_queries(invalid_query))

        self.assertListEqual(
            result, [
                {"queryId": 1, "results": []},
                {"queryId": 2, "results": [{"result": 3}]}
            ]
        )

    def test_handle_results_store(self):
        query_obj = factories.QueryFactory()
        factories.QueryFactory(data=[self.invalid_item])

        results_json = json.dumps(
            [{"queryId": query_obj.id, "results": [{"result": 3}]}])

        handle_results(results_json)
        result_obj = Result.objects.first()

        self.assertEqual(Result.objects.count(), 1)
        self.assertEqual(result_obj.id, query_obj.result.id)

    def test_valid_and_invalid_queries_handled_count(self):
        valid_count = 5
        invalid_count = 2
        factories.QueryFactory.create_batch(valid_count)
        factories.QueryFactory(
            data=[self.invalid_item for _ in range(invalid_count)])

        queries = Query.get_unhandled_queries()

        results = handle_queries(json.dumps(queries))
        handle_results(results)

        self.assertEqual(Result.objects.count(), valid_count + 1)
        self.assertEqual(QueryException.objects.count(), invalid_count)
