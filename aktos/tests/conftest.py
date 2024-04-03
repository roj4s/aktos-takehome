import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from .factories import ConsumerFactory, AccountFactory

register(ConsumerFactory)
register(AccountFactory)

@pytest.fixture
def api_client():
    return APIClient
