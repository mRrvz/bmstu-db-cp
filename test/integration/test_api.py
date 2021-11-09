""" Test API module """

import requests
import json
import pytest

default_app_url = "http://0.0.0.0:5000"

@pytest.fixture(scope="function")
def clear_cache():
    url = f"{default_app_url}/api/v1/cache/clear"
    response = requests.put(url)
    assert response.status_code == 200


def test_update(clear_cache):
    pass


def test_remove(clear_cache):
    pass


def test_save(clear_cache):
    return
    url = f"{default_app_url}/api/v1/rpd"
    data = json.dumps({"filename": "/files/rpd_example_01.docx"})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=data, headers=headers)

    assert response.status_code == 200
    json_object = json.loads(response.text)
    object_id = json_object["data"]["id"]

    url = f"{default_app_url}/api/v1/rpd/{object_id}"
    response = requests.get(url)
    assert response.status_code == 200
    assert json_object["data"] == json.loads(response.text)["data"]
