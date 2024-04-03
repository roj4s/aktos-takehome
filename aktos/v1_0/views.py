from django.db.models import QuerySet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import Response
from .serializers import AccountDefaultSerializer, AccountGetSerializer, ConsumerSerializer, CsvUploadSerializer
from .models import Consumer, ConsumerBalance, StatusChoises
from typing import Any, Type, Union
import pandas as pd


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

class UploadCsvView(generics.CreateAPIView):
    serializer_class = CsvUploadSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        status_map = {}

        for choice in StatusChoises.choices:
            key = "_".join(choice[1].upper().split(" "))
            status_map[key] = choice[0]

        for _, row in reader.iterrows():
            consumer_ssn = row['ssn']
            consumer = Consumer.objects.filter(ssn=consumer_ssn).first()
            if consumer is None:
                consumer = Consumer.objects.create(name=row["consumer name"], ssn=row["ssn"], address=row["consumer address"])
            ConsumerBalance.objects.create(client_reference_no=row["client reference no"], balance=float(row["balance"]), status=status_map[row["status"]], consumer=consumer)

        return Response({"status": "sucess"}, status.HTTP_201_CREATED)
