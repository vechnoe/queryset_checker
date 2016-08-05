from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden

from checker.models import Query
from checker.forms import QueryForm
from checker.tasks import process_chain


class QueryListView(FormView, ListView):
    model = Query
    form_class = QueryForm
    object_list = Query.objects.all()

    def get_context_data(self, **kwargs):
        context = super(QueryListView, self).get_context_data(**kwargs)
        context['latest_status'] = self.model.get_latest_status()
        context['form'] = self.get_form()
        context['queries_exists'] = len(Query.get_unhandled_queries()) > 0
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse('checker:query_list')

    def form_valid(self, form):
        query = Query()
        query.data = form.cleaned_data.get('data')
        query.save()
        messages.add_message(
            self.request, messages.SUCCESS, 'Your query saved')
        return redirect(self.get_success_url())


class ProcessView(LoginRequiredMixin, FormView):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            process_chain()
            return JsonResponse({'message': 'Processing started'}, status=200)
        return HttpResponseForbidden()


class QueryDetailView(DetailView):
    model = Query

    def get_context_data(self, **kwargs):
        context = super(QueryDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
