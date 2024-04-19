import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

DB_NAME = 'rlt'
COLLECTION_NAME = 'sample_collection'
MONGODB = "mongodb://localhost:27017/"

GROUP_TYPES = ['year', 'month', 'dayOfMonth', 'hour']

DATE_PATTERN = "%Y-%m-%dT%H:%M:%S"

MAX_LEN = 4096