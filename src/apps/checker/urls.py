from django.conf.urls import url
from checker.views import QueryListView, ProcessView, QueryDetailView

urlpatterns = [
    url(r'^$', QueryListView.as_view(), name='query_list'),
    url(r'process/$', ProcessView.as_view(), name='process_queries'),
    url(r'(?P<pk>\d+)/$', QueryDetailView.as_view(), name='query_detail'),
]
