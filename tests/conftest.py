import pytest


from olcf_api.client import OLCFAPIClient

@pytest.fixture
def client(requests_mock):
    client = OLCFAPIClient(api_token="XXX")
    json = {"foo": "bar"}
    requests_mock.post(client.base_url, json=json)
    return client
