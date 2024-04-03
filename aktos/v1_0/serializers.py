from rest_framework import serializers
from .models import Consumer, ConsumerBalance, StatusChoises


class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumer
        fields = ['ssn', 'name', 'address', 'created']


class AccountGetSerializer(serializers.ModelSerializer):
    consumer_ssn = serializers.CharField(source="consumer.ssn")
    consumer_name = serializers.CharField(source="consumer.name")
    consumer_address = serializers.CharField(source="consumer.address")
    status = serializers.SerializerMethodField()

    class Meta:
        model = ConsumerBalance
        fields = ("id", "client_reference_no", "balance", "status", "consumer_ssn", "consumer_name", "consumer_address", "created")

    def get_status(self, instance):
        return StatusChoises(instance.status).name


class AccountDefaultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerBalance
        fields = ("id", "client_reference_no", "balance", "status", "consumer", "created")


class CsvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
