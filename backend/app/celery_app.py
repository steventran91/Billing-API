import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
celery = Celery("billing-api", broker=REDIS_URL)
