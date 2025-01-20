from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """mysql db"""
    DB_USE: bool = False  # 是否启用MySQL
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_DATABASE: str = 'fastapi'
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


class RedisSettings(BaseSettings):
    """redis"""
    REDIS_USE: bool = False  # 是否启用Redis
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


class MongoSettings(BaseSettings):
    """mongodb"""
    MONGO_USE: bool = False  # 是否启用MongoDB
    MONGO_URI: str = 'mongodb://localhost:27017'
    MONGO_DB: str = 'fastapi'

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


myslq_settings = Settings()
redis_settings = RedisSettings()
mongo_settings = MongoSettings()
