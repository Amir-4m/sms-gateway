import logging

from celery import shared_task

from .models import Provider, SMSGateway
from .services import SMSGatewayService

logger = logging.getLogger(__name__)


@shared_task()
def send_message(sms_gateway_id, text, phone_numbers):
    sms_gateway = SMSGateway.objects.get(id=sms_gateway_id)
    provider = sms_gateway.provider
    logger.info(f'sending sms with sms_gateway {sms_gateway_id}, text: {text}, phone_numbers: {phone_numbers}')
    if provider.provider_code == Provider.CODE_RAHYAB:
        try:
            SMSGatewayService().rahyab_send_sms(sms_gateway, text, phone_numbers)
        except Exception as e:
            logger.error(f"sending message to {phone_numbers} with gateway {sms_gateway} failed: {e}")
