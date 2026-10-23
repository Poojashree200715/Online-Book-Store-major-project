from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from .models_newsletter import Subscriber


def subscribe_url():
    try:
        return reverse('subscribe')
    except NoReverseMatch:
        return reverse('store:subscribe')


class NewsletterTests(TestCase):
    def test_valid_email_is_saved(self):
        self.client.post(subscribe_url(), {'email': 'Test@Example.com'})
        self.assertTrue(Subscriber.objects.filter(email='test@example.com').exists())

    def test_duplicate_email_not_added_twice(self):
        for _ in range(2):
            self.client.post(subscribe_url(), {'email': 'a@b.com'})
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_invalid_email_rejected(self):
        self.client.post(subscribe_url(), {'email': 'not-an-email'})
        self.assertEqual(Subscriber.objects.count(), 0)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(subscribe_url()).status_code, 405)


class AdminTests(TestCase):
    def test_admin_requires_login(self):
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_superuser_can_see_subscribers(self):
        User.objects.create_superuser('admin', 'a@a.com', 'pass12345')
        self.client.login(username='admin', password='pass12345')
        self.assertEqual(self.client.get('/admin/store/subscriber/').status_code, 200)

    def test_csv_export(self):
        User.objects.create_superuser('admin', 'a@a.com', 'pass12345')
        Subscriber.objects.create(email='x@y.com')
        self.client.login(username='admin', password='pass12345')
        resp = self.client.post('/admin/store/subscriber/', {
            'action': 'export_csv',
            '_selected_action': [Subscriber.objects.first().pk],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'x@y.com', resp.content)
