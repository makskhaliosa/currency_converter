from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RatesSerializer
from .models import Rate


class RatesViewSet(APIView):
    """Вьюсет для запроса курса валют."""
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['from', 'to', 'value']

    def get(self, request):
        req_data = {
            'from_currency': request.query_params.get('from'),
            'to_currency': request.query_params.get('to'),
            'value': request.query_params.get('value')
        }
        rate = Rate(**req_data)
        serializer = RatesSerializer(rate)
        return Response(serializer.data, status=status.HTTP_200_OK)
