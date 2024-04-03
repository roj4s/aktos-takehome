from rest_framework import serializers
from .models import Consumer


class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumer
        fields = ['ssn', 'name', 'address']
