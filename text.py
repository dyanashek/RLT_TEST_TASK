START_MESSAGE = r'''
Введите свой запрос, например:

{
    "dt_from" : "2022-09-01T00:00:00",
    "dt_upto" : "2022-12-31T23:59:00",
    "group_type" : "month"
}

Допустимые group_type: year, month, day, hour.
'''

INPUT_ERROR = 'Недопустимые данные.'