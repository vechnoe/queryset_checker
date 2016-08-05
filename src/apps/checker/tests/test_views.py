from django.test import TestCase
from django.core.urlresolvers import reverse

from users.tests.factories import UserFactory

from checker.models import Query
from checker.forms import QueryForm


class CheckerViewsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def _log_in_and_test(self, user):
        if user is not None:
            logged_in = self.client.login(
                username=user.username, password='test')
            self.assertTrue(logged_in)

    def _test_query_list(self):
        response = self.client.get(reverse('checker:query_list'))
        self.assertEqual(response.status_code, 200)
        return response.context

    def test_query_list_with_form(self):
        context = self._test_query_list()
        self.assertIsInstance(context['form'], QueryForm)

    def test_invalid_query_form(self):
        response = self.client.post(
            reverse('checker:query_list'),
            {'data': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'data', 'This field is required.')

    def test_invalid_json_query_form(self):
        response = self.client.post(
            reverse('checker:query_list'),
            {'data': 'Hola'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'data', "'Hola' value must be valid JSON.")

    def test_post_to_valid_query_form(self):
        self.assertEqual(Query.objects.count(), 0)
        response = self.client.post(
            reverse('checker:query_list'),
            {'data': '{"a": 1}'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Query.objects.count(), 1)

    def test_process_view(self):
        self._log_in_and_test(self.user)

        response = self.client.post(
            reverse('checker:process_queries'), {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode(), '{"message": "Processing started"}')
