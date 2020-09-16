from rest_framework import views
from rest_framework.response import Response

from apps.services.api.authentications import ServiceAuthentication
from apps.services.api.permissions import ServicePermission

from .serializers import SendSMSSerializer
from ..tasks import send_message


class SendSMSAPIView(views.APIView):
    authentication_classes = (ServiceAuthentication,)
    permission_classes = (ServicePermission,)

    def post(self, request, *args, **kwargs):
        service = request.auth['service']
        serializer = SendSMSSerializer(data=request.data, context={'service': service})
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        phone_numbers = serializer.validated_data['phone_numbers']
        sms_gateway = serializer.validated_data['sms_gateway']

        send_message.delay(sms_gateway_id=sms_gateway.id, text=text, phone_numbers=phone_numbers)

        return Response('message created in queue.')
