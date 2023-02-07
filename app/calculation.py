import datetime
from calendar import Calendar


def deposite_calc(req_json) -> list:
    '''Расчёт роста депозита '''
    right_const = 1 + req_json['rate'] / 12 / 100 # правая часть формулы константа

    deposite_sum = [round(req_json['amount'] * right_const, 2)]

    for ind in range(req_json['periods'] - 1):
        summ = deposite_sum[ind] * right_const
        deposite_sum.append(round(summ, 2))

    return deposite_sum


def increase_days(req_json) -> list:
    '''Расчёт дней выплат - последний день месяца'''
    start_date = req_json['date']

    calendar = Calendar(0)
    inc_dates = []

    for month_shift in range(req_json['periods']):
        year = start_date.year
        month = (start_date.month + month_shift) % 12

        if month < start_date.month: # Если произошло переполнение месяца
            year += 1
            month += 1

        month_days = calendar.monthdayscalendar(year=year, month=month)
        last_day = max(month_days[-1])

        inc_dates.append(
            datetime.date(year, month, last_day).strftime('%d.%m.%Y')
        )
    
    return inc_dates