# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global settings for the application.
    """
    # app settings
    app_name: str
    app_version: str
    allowed_hosts: str
    api_key: str

    # database settings
    database_url: str

    # external data references
    crm_api_url: str
    marketing_api_url: str

    # model settings
    model_config = SettingsConfigDict(env_file=".env")


# instantiate the settings object
settings = Settings()