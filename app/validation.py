import datetime


deposite_schema = {
    'amount': {
        'type': int, 
        'constrains': lambda val: val >= 10e3 and val <= 3e6,
        'constrains_description': 'От 10 000 до 3 000 000'
        },
    'periods': {
        'type': int,
        'constrains': lambda val: val >= 1 and val <= 60,
        'constrains_description': 'От 1 до 60'
        },
    'rate': {
        'type': int,
        'constrains': lambda val: val >= 1 and val <= 8,
        'constrains_description': 'От 1 до 8'
        },
    'date': {
        'type': datetime.date,
        'constrains': lambda val: val.day >=28 and val.day <= 31, # Наверное дата должна быть последней в месяце
        'constrains_description': 'Дата должна быть последним днём месяца'
        }
}


def assert_err_to_false(func):
    '''AssertionError подменятеся на False'''
    def wrapper(req_json):
        try:
            return func(req_json)

        except AssertionError as e:
            return e.args[-1]

        except (ValueError, TypeError): # От невалидных дат
            return f'Поле "date" не соответствует формату "dd.mm.YYYY"'

    return wrapper


@assert_err_to_false
def validate_deposite(req_json: dict) -> str:
    '''Валидация наличия обязательных полей; типов полей; ограничений значений
    Возвращает:
        True - Если валидация пройдена
        str - Сообщение о причинах ошибки
    Обрабатываются декортаром:
        При AssertionError возвращается только текст ошибки
        ValueError может возникнуть при преобразовании строки в datetime'''

    temp_json = dict(                                                 # Являются ли лишние поля ошибкой?
        filter(lambda x: x[0] in deposite_schema, req_json.items())   # А если удалённые поля будут нужны для дальнейшей обратки?
    )                                                                 # Поэтому создаётся и фильтруется копия, а не исходный запрос

    assert temp_json.keys() == deposite_schema.keys(), \
        f'Переданы не все обязательные параметры, не хватает следующих: {set(temp_json) ^ set(deposite_schema)}'

    # Преобразование даты в объект, может вызвать ValueError - ловится декоратором как ошибка валидации
    req_json['date'] = datetime.datetime.strptime(temp_json['date'], '%d.%m.%Y').date() # Происходит именно после проверки что ключ date есть в запросе
    temp_json['date'] = req_json['date']

    for key in temp_json.keys():

        assert isinstance(temp_json[key], deposite_schema[key]['type']), \
            f'Поле {key} должно быть типа {deposite_schema[key]["type"]}'

        assert deposite_schema[key]['constrains'](temp_json[key]), \
            f'Поле {key} выходит за ограничения - {deposite_schema[key]["constrains_description"]}'

    return True
