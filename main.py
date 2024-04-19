import config

import asyncio
import motor.motor_asyncio
import datetime as dt


client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]


async def aggregate_data(start_date, end_date, group_type):
    start_date = dt.datetime.strptime(start_date, config.DATE_PATTERN)
    end_date = dt.datetime.strptime(end_date, config.DATE_PATTERN)

    if group_type == 'day':
        group_type = 'dayOfMonth'

    pipeline = await generate_pipeline(start_date, end_date, group_type)
    data = await collection.aggregate(pipeline).to_list(length=None)

    return data


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

print(asyncio.run(aggregate_data("2022-10-01T23:00:00", "2022-11-30T23:59:00", "day")))
