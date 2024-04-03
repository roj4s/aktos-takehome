from django.db.models import QuerySet
from rest_framework import permissions, viewsets
from .serializers import AccountDefaultSerializer, AccountGetSerializer, ConsumerSerializer
from .models import Consumer, ConsumerBalance, StatusChoises
from typing import Any, Type, Union


class ConsumerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows consumers to be viewed or edited.
    """
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset: QuerySet[ConsumerBalance] = ConsumerBalance.objects.all()
    def get_serializer_class(self) -> Union[Type[AccountDefaultSerializer], Type[AccountGetSerializer]]:
        if self.request.method == "GET":
            return AccountGetSerializer

        return AccountDefaultSerializer

    def get_queryset(self) -> QuerySet[ConsumerBalance]:
        query = ConsumerBalance.objects
        query_params: dict[str, Any] = self.request.query_params

        min_balance = query_params.get("min_balance")
        max_balance = query_params.get("max_balance")
        consumer_name = query_params.get("consumer_name")
        status = query_params.get("status")

        if min_balance is not None:
            query = query.filter(balance__gte=float(min_balance))

        if max_balance is not None:
            query = query.filter(balance__lte=float(max_balance))

        if consumer_name is not None:
            query = query.filter(consumer__name=consumer_name)

        if status is not None:
            query = query.filter(status=status)

        return query.filter()

