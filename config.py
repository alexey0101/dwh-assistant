import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    PG_DBNAME = os.getenv("PG_DBNAME")
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")

    YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
    YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

    TABLE_NAMES = [table.strip() for table in os.getenv('TABLE_NAMES', '').split(',') if table.strip()]
