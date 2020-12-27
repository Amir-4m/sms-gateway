import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.test import RequestFactory, override_settings
from django.urls import reverse
from django.utils.encoding import force_text
from mock import patch
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from apps.services.models import Service


class SendSMSBaseAPITestCase(APITestCase):
    fixtures = ['gateway', 'service']

    def setUp(self):
        self.service = Service.objects.first()
        self.client = APIClient()
        self.request = RequestFactory()
        self.request.auth = {'service': self.service}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.service.secret_key))
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)


@override_settings(CACHES=settings.TEST_CACHES)
class SendSMSAPITestCase(SendSMSBaseAPITestCase):
    @patch('apps.gateway.tasks.send_message.delay')
    def test_post_sms_valid(self, mock_method):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['09123456789']}]
        }
        response = self.client.post(url, data=data, format='json')
        response_data = json.loads(force_text(response.content))

        self.assertEqual(response_data, "messages created in queue.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_method.assert_called_once_with(
            sms_gateway_id=self.service.gateways.filter(
                provider__is_enable=True,
                is_enable=True).order_by('priority').first().id,
            text='this is a test message.',
            phone_numbers=['09123456789']
        )

    @patch('apps.gateway.tasks.send_message.delay')
    def test_post_sms_valid_head_number(self, mock_method):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['09123456789']}],
            'head_number': '1000'
        }
        response = self.client.post(url, data=data, format='json')
        response_data = json.loads(force_text(response.content))

        self.assertEqual(response_data, "messages created in queue.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_method.assert_called_once_with(
            sms_gateway_id=self.service.gateways.filter(
                provider__is_enable=True,
                is_enable=True).order_by('priority').first().id,
            text='this is a test message.',
            phone_numbers=['09123456789']
        )

    def test_post_sms_invalid_head_number(self):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['09123456789']}],
            'head_number': '0000'
        }
        response = self.client.post(url, data=data, format='json')

        self.assertRaisesMessage(
            ValidationError,
            'provider with this head number does not exists!'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_sms_invalid(self):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['0912345']}]
        }
        service = Service.objects.last()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(service.secret_key))
        response = client.post(url, data=data, format='json')
        self.assertContains(
            response,
            'enter phone_number in the correct form!',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_post_sms_no_gateway(self):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['09123456789']}]
        }
        service = Service.objects.last()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(service.secret_key))
        response = client.post(url, data=data, format='json')

        self.assertContains(
            response,
            'there is no available sms gateway for this service!',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ServiceThrottleTestCase(SendSMSBaseAPITestCase):
    def setUp(self):
        super(ServiceThrottleTestCase, self).setUp()
        cache.clear()

    @patch('apps.gateway.tasks.send_message.delay')
    def test_post_sms_throttled(self, mock_method):
        url = reverse('send-message')
        data = {
            'data': [{'text': 'this is a test message.', 'phone_numbers': ['09123456789']}]
        }
        for _ in range(2):
            response = self.client.post(url, data=data, format='json')

        self.assertRaisesMessage(
            AssertionError,
            "Request was throttled. Expected available in 60 seconds."
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        mock_method.assert_called_once_with(
            sms_gateway_id=self.service.gateways.filter(
                provider__is_enable=True,
                is_enable=True).order_by('priority').first().id,
            text='this is a test message.',
            phone_numbers=['09123456789']
        )
