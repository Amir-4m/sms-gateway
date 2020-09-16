import zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from .models import SentMessage


class SMSGatewayService:
    transport = Transport(cache=InMemoryCache())

    def rahyab_send_sms(self, sms_gateway, text, phone_numbers):
        wsdl = sms_gateway.provider.properties.get('url')
        username = sms_gateway.provider.properties.get('username')
        password = sms_gateway.provider.properties.get('password')
        head_number = sms_gateway.provider.head_number
        data = {
            "username": username,
            "password": password,
            "from": str(head_number),
            "to": phone_numbers,
            "text": text,
            "isflash": False,
            "udh": ""
        }
        client = zeep.Client(wsdl=wsdl, transport=self.transport)
        result = client.service.SendSms(**data)
        return SentMessage.objects.create(
            sms_gateway=sms_gateway,
            target_numbers=phone_numbers,
            status=str(result.status.byte[0]),
            recipient_id=str(result.recId.long[0])
        )
