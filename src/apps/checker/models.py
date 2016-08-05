from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import JSONField


class Query(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.NullBooleanField(null=True)
    data = JSONField(verbose_name='Data set', default='')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __str__(self):
        return 'ID: %d at %s' % (
            self.id, timezone.localtime(
                self.date).strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def get_latest_status(cls):
        queryset = cls.objects.filter(
            Q(status=True) |
            Q(status=False))
        if queryset.exists():
            return queryset.first().status
        return None

    @classmethod
    def get_unhandled_queries(cls):
        return list(cls.objects.filter(status=None).values('id', 'data'))

    @classmethod
    def update_statuses(cls):
        cls.objects.filter(
            result__isnull=False).distinct().update(status=True)
        cls.objects.filter(
            exceptions__isnull=False).distinct().update(status=False)


class Result(models.Model):
    query = models.OneToOneField(Query, related_name='result')
    result = JSONField(verbose_name='Data set', default='')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return str(self.id)


class QueryException(models.Model):
    query = models.ForeignKey(
        Query, verbose_name='Query set', related_name='exceptions')
    date = models.DateTimeField(auto_now_add=True)
    traceback = models.TextField(default='')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Query Exception'
        verbose_name_plural = 'Query Exceptions'

    def __str__(self):
        return '%s at %s' % (
            self.traceback.split(' ')[0], timezone.localtime(
                self.date).strftime('%Y-%m-%d %H:%M:%S'))
