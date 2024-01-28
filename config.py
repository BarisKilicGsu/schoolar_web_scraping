import os
from dotenv import load_dotenv


class Settings:

    load_dotenv()


    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    API_PORT = os.getenv('API_PORT')
    API_HOST = os.getenv('API_HOST')

settings = Settings()
