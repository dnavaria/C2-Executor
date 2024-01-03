import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv(".env")


def get_public_ip():
    try:
        response = urllib.request.urlopen('https://httpbin.org/ip')
        data = json.loads(response.read().decode())
        return data['origin']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    C2_EXECUTOR_QUEUE = os.getenv("C2_EXECUTOR_QUEUE")
    WORKER_CONCURRENCY = os.getenv("WORKER_CONCURRENCY")
    WORKER_POOL = os.getenv("WORKER_POOL")
    WORKER_NAME = f"c2_worker@{get_public_ip()}"
