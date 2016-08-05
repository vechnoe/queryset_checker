import json

from celery import chain

from src import celery_app
from checker.utils import handle_queries, handle_results
from checker.models import Query


@celery_app.task
def read_queries():
    queries = json.dumps(Query.get_unhandled_queries())
    return queries


@celery_app.task
def test_func(queries):
    return handle_queries(queries)


@celery_app.task
def store_result(results):
    handle_results(results)


def process_chain():
    chain(read_queries.s() | test_func.s() | store_result.s()).apply_async()
