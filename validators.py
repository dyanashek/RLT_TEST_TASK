import json
import datetime as dt


import config


async def date_validator(start_date, end_date):
    try:
        start_date = dt.datetime.strptime(start_date, config.DATE_PATTERN)
        end_date = dt.datetime.strptime(end_date, config.DATE_PATTERN)
    except:
        return False, False

    if start_date > end_date:
        return False, False
    
    return start_date, end_date


async def type_validator(group_type):
    if group_type == 'day':
        group_type = 'dayOfMonth'
    
    if group_type in config.GROUP_TYPES:
        return group_type
    
    return False


async def input_validator(message):
    try:
        request = json.loads(message)
        start_date = request['dt_from']
        end_date = request['dt_upto']
        group_type = request['group_type']
    except:
        return False, False, False

    start_date, end_date = await date_validator(start_date, end_date)
    group_type = await type_validator(group_type)
    
    return start_date, end_date, group_type