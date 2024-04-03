import pytest
import json

pytestmark = pytest.mark.django_db

class TestConsumersEndpoint:
    endpoint = "/consumers"

    def test_get(self, consumer_factory, api_client):
        consumer_factory()
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_post_wrong_ssn(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "wrong_ssn", "name": "John Doe", "address": "Random Street # 34"})
        assert response.status_code == 400

    def test_post_missing_fields(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "018-79-4253"})
        assert response.status_code == 400

    def test_post(self, api_client):
        response = api_client().post(self.endpoint, {"ssn": "018-79-4253", "name": "John Doe", "address": "Random Street # 34"})
        assert response.status_code == 201
