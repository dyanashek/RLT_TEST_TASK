import json
import motor.motor_asyncio
import datetime as dt
from dateutil.rrule import rrule, HOURLY, DAILY, MONTHLY, YEARLY


import config


client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]


PERIODS = {
    'year' : YEARLY,
    'month' : MONTHLY,
    'dayOfMonth' : DAILY,
    'hour' : HOURLY,
}


async def aggregate_data(start_date, end_date, group_type):
    if group_type == 'day':
        group_type = 'dayOfMonth'

    iterator_start_date = await generate_iterator_start_date(start_date, group_type)

    pipeline = await generate_pipeline(start_date, end_date, group_type)
    data = await collection.aggregate(pipeline).to_list(length=None)

    result = {
        'dataset' : [],
        'labels' : [],
    }

    counter = 0

    for num, date in enumerate(rrule(PERIODS[group_type], dtstart=iterator_start_date, until=end_date)):
        try:
            label = dt.datetime.strptime(data[counter].get('label'), config.DATE_PATTERN)
        except:
            label = None

        if num == 0:
            result['labels'].append(start_date.isoformat())
        else:
            result['labels'].append(date.isoformat())

        if label and label == date:
            result['dataset'].append(data[counter].get('total_value'))
            counter += 1

        else:
            result['dataset'].append(0)

            
    
    return json.dumps(result)


async def generate_pipeline(start_date, end_date, group_type):
    pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": {},
                    "total_value": {"$sum": "$value"},
                }
            },
            {
                "$addFields": {
                    "label": {
                        "$concat": [
                            {"$toString": "$_id.year"},
                            "-",
                            {"$toString": {"$ifNull": ["$_id.month", "1"]}},
                            "-",
                            {"$toString": {"$ifNull": ["$_id.dayOfMonth", "1"]}},
                            "T",
                            {"$toString": {"$ifNull": ["$_id.hour", "0"]}},
                            ":00:00"
                        ]
                    }
                }
            },
            {"$sort": {}},
        ]

    for time_period in config.GROUP_TYPES:
        pipeline[1]['$group']['_id'][time_period] = {f'${time_period}' : '$dt'}
        pipeline[-1]['$sort'][f'_id.{time_period}'] = 1
        if time_period == group_type:
            break
    
    return pipeline


async def generate_iterator_start_date(start_date, group_type):
    year =start_date.year
    month = start_date.month
    day = start_date.day
    hour = start_date.hour

    group_types = {
        'year' : year,
        'month' : month,
        'dayOfMonth' : day,
        'hour' : hour,
    }

    start_date_args = []

    for time_period in config.GROUP_TYPES:
        start_date_args.append(group_types[time_period])

        if time_period == group_type:
            break
    
    return await generate_date(*start_date_args)


async def generate_date(year, month = 1, day = 1, hour = 0):
    return dt.datetime(year, month, day, hour)
