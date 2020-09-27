from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.response import Response

from apps.services.api.authentications import ServiceAuthentication
from apps.services.api.permissions import ServicePermission

from .serializers import SendSMSSerializer
from .throttles import ServiceThrottle
from ..tasks import send_message


class SendSMSAPIView(views.APIView):
    authentication_classes = (ServiceAuthentication,)
    permission_classes = (ServicePermission,)
    throttle_classes = (ServiceThrottle,)

    @swagger_auto_schema(
        operation_description='get a list of text - numbers and send the text to each number in the array',
        request_body=SendSMSSerializer,
        responses={200: "messages created in queue."}
    )
    def post(self, request, *args, **kwargs):
        service = request.auth['service']
        serializer = SendSMSSerializer(data=request.data, context={'service': service})
        serializer.is_valid(raise_exception=True)
        sms_gateway = serializer.validated_data['sms_gateway']
        for data in serializer.validated_data['data']:
            send_message.delay(sms_gateway_id=sms_gateway.id, text=data['text'], phone_numbers=data['phone_numbers'])

        return Response('messages created in queue.')
