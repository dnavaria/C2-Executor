import os
from dotenv import load_dotenv

load_dotenv(".env")


class Settings:
    API_SERVER_HOST = os.getenv("API_SERVER_HOST")
    API_SERVER_PORT = int(os.getenv("API_SERVER_PORT"))

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    POSTGRES_URL = os.getenv("POSTGRES_URL")
    REDIS_URL = os.getenv("REDIS_URL")

    C2_EXECUTOR_QUEUE = os.getenv("C2_EXECUTOR_QUEUE")
