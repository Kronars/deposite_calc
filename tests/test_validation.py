from collections import OrderedDict

import pytest
from flask.testing import FlaskClient


def test_unfilled_req(client: FlaskClient):
    '''Недостающие поля запроса должны быть возвращены в тексте ошибки'''
    unfilled_req = {"amount":10000}

    response = client.post('/deposite/', json=unfilled_req)

    answer_el = {'date', 'periods', 'rate'}

    # Парсинг словаря из строки ->
    # "Переданы не все обязательные параметры, не хватает следующих: {'date', 'periods', 'rate'}"
    resp_unfilled_el = response.json['error'].split(': ')[1]
    resp_unfilled_el = eval(resp_unfilled_el)

    assert response.status_code == 400
    assert resp_unfilled_el == answer_el


def test_overfilled_req(client: FlaskClient):
    '''Лишния поля в запросе должны игнорироваться'''
    overfilled_req = {
        "а я лишний параметр":"очень лишний",
        "amount":10000,
        "periods":4,
        "rate":1,
        "date":"31.10.2021",
        "test":"test"
    }
    answer = {
        '31.10.2021': 10008.33, 
        '30.11.2021': 10016.67, 
        '31.01.2022': 10025.02, 
        '28.02.2022': 10033.37
    }

    response = client.post('/deposite/', json=overfilled_req)

    assert response.status_code == 200
    assert OrderedDict(response.json) == OrderedDict(answer) # Почему бы заодно и не проверить порядок


@pytest.mark.parametrize(
    ('input_test', 'expected'),
    (
        ({'key': 'amount', 'val': -1}, ['amount', 'От 10 000 до 3 000 000']),
        ({'key': 'amount', 'val': int(3e6 + 1)}, ['amount', 'От 10 000 до 3 000 000']), # если float то падает
        ({'key': 'periods', 'val': 0}, ['periods', 'От 1 до 60']),
        ({'key': 'periods', 'val': 61}, ['periods', 'От 1 до 60']),
        ({'key': 'rate', 'val': -10}, ['rate', 'От 1 до 8']),
        ({'key': 'rate', 'val': 10}, ['rate', 'От 1 до 8']),
        ({'key': 'date', 'val': '27.01.2001'}, ['date', 'Дата должна быть последним днём месяца'])
    )
)
def test_field_restriction(client: FlaskClient, input_test, expected):
    '''Проверка ограничений полей'''
    data = {
        "amount":10000,
        "periods":4,
        "rate":8,
        "date":"31.10.2021"
    }

    # Подстановка параметров в запрос
    data[input_test['key']] = input_test['val'] 

    response = client.post('/deposite/', json=data)

    for text in expected:
        assert response.status_code == 400
        assert text in str(response.json) # В тексте ошибки должно встречаться ошибочное поле, текст ограничения


@pytest.mark.parametrize(
    ('input_test', 'expected'),
    (
        ({'key': 'amount', 'val': '10000'}, ['amount', 'int']),
        ({'key': 'date', 'val': 10}, ['date', 'dd.mm.YYYY'])
    )
)
def test_filed_types(client: FlaskClient, input_test, expected):
    '''Неверный тип полей должен возвращать ошибку с указанием неправильного типа поля'''
    data = {
        "amount":10000,
        "periods":4,
        "rate":8,
        "date":"31.10.2021"
    }

    # Подстановка параметров в запрос
    data[input_test['key']] = input_test['val'] 

    response = client.post('/deposite/', json=data)

    for text in expected:
        assert response.status_code == 400
        assert text in str(response.json)
