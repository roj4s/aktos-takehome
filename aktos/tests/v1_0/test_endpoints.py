import pytest
import json

pytestmark = pytest.mark.django_db

class TestConsumersEndpoint:
    endpoint = "/consumers"

    def test_get(self, consumer_factory, api_client):
        consumer_factory()
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1

    def test_post_wrong_ssn(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "wrong_ssn", "name": "John Doe", "address": "Random Street # 34"})
        assert response.status_code == 400

    def test_post_missing_fields(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "018-79-4253"})
        assert response.status_code == 400

    def test_post(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "018-79-4253", "name": "John Doe", "address": "Random Street # 34"})
        assert response.status_code == 201

class TestAccountsEndpoint:
    endpoint = "/accounts"

    def test_get(self, account_factory, api_client):
        account_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 4
        entry = data[0]
        assert "consumer_name" in entry
        assert "consumer_ssn" in entry
        assert "consumer_address" in entry
        assert "balance" in entry

    def test_get_min_max_balance(self, account_factory, api_client):
        account_factory.create_batch(10)
        response = api_client().get(f"{self.endpoint}?min_balance=40&max_balance=80")
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 5
        assert data[0]["balance"] == 80
        assert data[-1]["balance"] == 40

    def test_get_filter_status(self, account_factory, api_client):
        account_factory.create_batch(10)
        response = api_client().get(f"{self.endpoint}?status=1")
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 10

        response = api_client().get(f"{self.endpoint}?status=3")
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 0

    def test_get_filter_consumer_name(self, account_factory, api_client):
        account_factory()
        response = api_client().get(f"{self.endpoint}?consumer_name=Jessica%20Williams")
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 1

        response = api_client().get(f"{self.endpoint}?consumer_name=unknown")
        assert response.status_code == 200
        data = json.loads(response.content)["results"]
        assert len(data) == 0
