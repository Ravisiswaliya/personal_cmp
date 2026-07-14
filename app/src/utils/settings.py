from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_TIME: int
    GOOGLE_APP_PASSWORD: SecretStr
    GMAIL_USERNAME: str


settings = Settings()
