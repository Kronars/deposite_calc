from collections import OrderedDict

from flask.testing import FlaskClient


def test_deposite_base_case(client: FlaskClient):
    '''Нормальное поведение'''
    data = {
        "amount":10000,
        "periods":7,
        "rate":6,
        "date":"31.01.2021"
    }

    answer = {
        "31.01.2021": 10050.0,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75,
        "30.04.2021": 10201.5,
        "31.05.2021": 10252.51,
        "30.06.2021": 10303.77,
        "31.07.2021": 10355.29
}

    resp = client.post('/deposite/', json=data)

    assert resp.status_code == 200
    assert OrderedDict(resp.json) == OrderedDict(answer)


def test_deposite_dates_boundary(client: FlaskClient):
    '''Проверка корректности дат на границе года'''
    data = {
        "amount":10000,
        "periods":4,
        "rate":8,
        "date":"31.10.2021"
    }

    answer = {
        "31.10.2021": 10066.67,
        "30.11.2021": 10133.78,
        "31.01.2022": 10201.34,
        "28.02.2022": 10269.35
    }

    resp = client.post('/deposite/', json=data)

    assert resp.status_code == 200
    assert OrderedDict(resp.json) == OrderedDict(answer)
