import sys
import traceback
import json

from checker.models import Query, Result, QueryException


def _result(item, _id):
    try:
        return dict(result=item['a'] + item['b'])
    except Exception:
        _type, _value, _traceback = sys.exc_info()

        _tb = '%s\n%s' % (
            traceback.format_exception_only(_type, _value)[0], str(item))
        ex = QueryException()
        ex.query_id = _id
        ex.traceback = _tb
        ex.save()
        return None


def check_func(query):
    _id = query['id']
    return [_result(item, _id) for item in query['data']]


def _handle_item(query):
    results = list(filter(None, check_func(query)))
    return dict(queryId=query['id'], results=results)


def handle_queries(json_data):
    queries = json.loads(json_data)
    return json.dumps([_handle_item(q) for q in queries])


def handle_results(json_data):
    data = json.loads(json_data)

    results = [
        Result(
            query_id=item['queryId'],
            result=item['results']
        )
        for item in data if item
    ]
    Result.objects.bulk_create(results)
    Query.update_statuses()
