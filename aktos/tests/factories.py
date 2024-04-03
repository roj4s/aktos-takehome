import factory
from v1_0.models import Consumer, ConsumerBalance
from faker.providers import ssn as fake_ssn
from faker import Faker

consumer_test_data = {
    "name": "Jessica Williams",
    "address": "0233 Edwards Glens Allisonhaven, HI 91491"
}

account_test_data = {
    "client_reference_no": "553efdb3-2baf-4c2a-88e2-7417d6bb0409",
    "status": 1,
}

class ConsumerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Consumer

    ssn = factory.Sequence(lambda n: Faker().ssn())
    name = consumer_test_data["name"]
    address = consumer_test_data["address"]

class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ConsumerBalance

    client_reference_no = account_test_data["client_reference_no"]
    balance = factory.Sequence(lambda n: 10 * n)
    status = account_test_data["status"]
    consumer = factory.SubFactory(ConsumerFactory)
