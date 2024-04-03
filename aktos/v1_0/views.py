from rest_framework import permissions, viewsets
from .serializers import ConsumerSerializer
from .models import Consumer


class ConsumerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows consumers to be viewed or edited.
    """
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
