import json
import logging

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.encoding import force_text
from mock import patch
from rest_framework import status
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
