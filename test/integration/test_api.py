""" Test API module """

import requests
import json
import pytest

from utils import default_app_url
# export PYTHONPATH=. pytest

def test_get():
    url = f"{default_app_url}/dpw/6"
    response = requests.get(url)
    expected = {
        'code': 200,
        'data': {'author': 'Author03',
            'competency': 'Competency03',
            'discipline_material': None,
            'discipline_module': None,
            'discipline_scope': None,
            'educational_program': None,
            'id': 6,
            'learning_outcomes': None,
            'name': 'Name03'
        },
        'message': None
    }

    assert response.status_code == 200
    assert json.loads(response.text) == expected


def test_update():
    pass


def test_remove():
    pass


def test_save():
    pass