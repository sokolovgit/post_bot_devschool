from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=('.env', 'stack.env'), env_file_encoding='utf-8', extra='ignore')


settings = Settings()
