from pydantic_settings import BaseSettings, SettingsConfigDict
from config.config import settings as app_settings

"""
配置参考loguru
"""


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = app_settings.BASE_PATH + "/storage/logs/fastapi-{time:YYYY-MM-DD}.log"
    LOG_RETENTION: str = "14 days"

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()
