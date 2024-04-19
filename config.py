import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

DB_NAME = 'rlt'
COLLECTION_NAME = 'sample_collection'

GROUP_TYPES = ['year', 'month', 'dayOfMonth', 'hour']

MONGODB = "mongodb://localhost:27017/"

DATE_PATTERN = "%Y-%m-%dT%H:%M:%S"

MAX_LEN = 4096