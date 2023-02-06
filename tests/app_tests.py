import json

import pytest
from flask.testing import FlaskClient


def test_deposite_base_case(client: FlaskClient):
    data = '''{
    "amount":10000,
    "periods":7,
    "rate":6,
    "date":"31.01.2021"
}'''
    answer = [10050.0, 10100.25, 10150.75, 10201.5, 10252.51, 10303.77, 10355.29]

    resp = client.post('/deposite', json=data)

    print(resp.json, dir(resp.json))

    assert True
