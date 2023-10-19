import os

from dotenv import dotenv_values, find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    STATIC_DIRECTORY: str = "../static"
    MONGO_URL: str = "mongodb://localhost:27017"
    BASE_URL: str = "http://localhost:8000"


config = Config()
