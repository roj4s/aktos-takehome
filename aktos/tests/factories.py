import factory
from v1_0.models import Consumer

consumer_test_data = {
    "ssn": "015-79-4253",
    "name": "Jessica Williams",
    "address": "0233 Edwards Glens Allisonhaven, HI 91491"
}

class ConsumerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Consumer

    ssn = consumer_test_data["ssn"]
    name = consumer_test_data["name"]
    address = consumer_test_data["address"]
