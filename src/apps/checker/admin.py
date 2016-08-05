from django.utils import timezone
from django.contrib import admin

from checker.models import Query, Result, QueryException


class QueryAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['date']
        else:
            return []

    def _start_date(self, obj):
        return timezone.localtime(
            obj.date).strftime('%Y-%m-%d')

    def _start_time(self, obj):
        return timezone.localtime(
            obj.date).strftime('%H:%M:%S')

    _start_time.short_description = 'Time'
    _start_date.short_description = 'Date'
    list_display = (
        'id', '_start_time', '_start_date', 'status')


class ResultAdmin(admin.ModelAdmin):
    def _query(self, obj): return obj.query.id

    _query.short_description = 'Query ID'

    list_display = ('_query',)


class QueryExceptionAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['date']
        else:
            return []

    def _start_date(self, obj):
        return timezone.localtime(
            obj.date).strftime('%Y-%m-%d')

    def _start_time(self, obj):
        return timezone.localtime(
            obj.date).strftime('%H:%M:%S')

    def _name(self, obj):
        return obj.traceback.split(' ')[0]

    _start_time.short_description = 'Time'
    _start_date.short_description = 'Date'
    _name.short_description = 'Exception'
    list_display = (
        'id', '_start_time', '_start_date', '_name')


admin.site.register(Query, QueryAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(QueryException, QueryExceptionAdmin)
