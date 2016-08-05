import sys
import traceback
import json

from checker.models import Query, Result, QueryException


def _result(item, _id, _exceptions):
    try:
        return dict(result=item['a'] + item['b'])
    except Exception:
        _type, _value, _traceback = sys.exc_info()

        _tb = '%s\n%s' % (
            traceback.format_exception_only(_type, _value)[0], str(item))
        ex = QueryException()
        ex.query_id = _id
        ex.traceback = _tb
        _exceptions.append(ex)
        return None


def check_func(query, _exceptions):
    _id = query['id']
    _out = [_result(item, _id, _exceptions) for item in query['data']]
    return _out


def _handle_item(query, _exceptions):
    results = list(filter(None, check_func(query, _exceptions)))
    return dict(queryId=query['id'], results=results)


def handle_queries(json_data):
    queries = json.loads(json_data)
    _exceptions = []
    _out = json.dumps([_handle_item(q, _exceptions) for q in queries])
    QueryException.objects.bulk_create(_exceptions)
    return _out


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
